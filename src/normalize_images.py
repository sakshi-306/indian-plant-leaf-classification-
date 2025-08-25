import os, glob, argparse
import numpy as np
import cv2
from PIL import Image
import pillow_heif

def normalize_image(img_path, target_size=(252, 252)):
    name_lower = img_path.lower()
    if name_lower.endswith(".heic"):
        heif = pillow_heif.open_heif(img_path)
        data = heif.data[0] if hasattr(heif, "data") and isinstance(heif.data, (list, tuple)) else heif.data
        img = Image.frombytes(heif.mode, heif.size, data)
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError("OpenCV failed to read image")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    img = img.astype(np.float32) / 255.0
    return img

def process_images(input_folder, output_folder, target_size=(252, 252)):
    os.makedirs(output_folder, exist_ok=True)
    patterns = ["*.png", "*.jpg", "*.jpeg", "*.heic", "*.HEIC", "*.JPG", "*.PNG", "*.JPEG"]
    image_files = []
    for ext in patterns:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))
    for path in image_files:
        try:
            normalized = normalize_image(path, target_size)
            out = (normalized * 255).astype(np.uint8)
            fname = os.path.basename(path)
            save_path = os.path.join(output_folder, fname)
            cv2.imwrite(save_path, cv2.cvtColor(out, cv2.COLOR_RGB2BGR))
            print(f"✅ Processed: {fname}")
        except Exception as e:
            print(f"❌ Error processing {path}: {e}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--img_size", nargs=2, type=int, default=[252, 252])
    args = ap.parse_args()
    process_images(args.input, args.output, target_size=tuple(args.img_size))
