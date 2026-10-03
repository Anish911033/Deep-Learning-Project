import base64, io, os
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, jsonify

IMG_SIZE = 256
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "unet_glas.keras")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB uploads

_model = None
def get_model():
    # Lazy-load so the server binds to its port quickly (Render health check)
    global _model
    if _model is None:
        import tensorflow as tf
        _model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return _model

def to_b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return "ok"

@app.route("/predict", methods=["POST"])
def predict():
    f = request.files.get("image")
    if not f:
        return jsonify(error="No image uploaded"), 400
    try:
        orig = Image.open(f.stream).convert("RGB")
    except Exception:
        return jsonify(error="Invalid image file"), 400

    small = orig.resize((IMG_SIZE, IMG_SIZE))
    x = np.asarray(small, dtype=np.float32)[None] / 255.0
    prob = get_model().predict(x, verbose=0)[0, ..., 0]
    mask = (prob > 0.5).astype(np.uint8)

    mask_img = Image.fromarray(mask * 255)
    overlay = np.asarray(small).copy()
    overlay[mask == 1] = (0.6 * overlay[mask == 1] + 0.4 * np.array([255, 0, 0])).astype(np.uint8)

    return jsonify(
        mask=to_b64(mask_img),
        overlay=to_b64(Image.fromarray(overlay)),
        gland_coverage=round(float(mask.mean()) * 100, 2),
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
