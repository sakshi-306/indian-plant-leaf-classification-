import os
import requests
import zipfile

# Small sample dataset (for testing only, not full project training)
URL = "https://github.com/dataprofessor/data/raw/master/plant_disease_small.zip"
OUT_PATH = "plant_disease_small.zip"
DEST_DIR = "datasets/"

def download_file(url, out_path):
    print(f"⬇️ Downloading dataset from {url} ...")
    r = requests.get(url, stream=True)
    with open(out_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("✅ Download complete!")

def extract_file(zip_path, extract_to=DEST_DIR):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✅ Extracted dataset into {extract_to}")

if __name__ == "__main__":
    download_file(URL, OUT_PATH)
    extract_file(OUT_PATH, DEST_DIR)
    print("🎉 Sample dataset ready in datasets/ folder!")
