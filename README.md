# Deploy on Render
1. In Colab, run `save_model_snippet.py` as a new cell; place the file at `model/unet_glas.keras`.
2. Push this folder to a GitHub repo (model is ~8 MB, fine for git).
3. Render dashboard -> New -> Blueprint (uses render.yaml) or New -> Web Service.
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --workers 1 --threads 2 --timeout 180`
4. Open the URL once it's live.

Local test: `pip install -r requirements.txt && python app.py`
