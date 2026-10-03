# Add this as a NEW CELL at the end of your notebook (after training), then run it.
# Use the same Keras version family as requirements.txt (Keras 3 / TF 2.16) when possible.
model.save("unet_glas.keras")

from google.colab import files
files.download("unet_glas.keras")
# Put the downloaded file in:  glas-render/model/unet_glas.keras
