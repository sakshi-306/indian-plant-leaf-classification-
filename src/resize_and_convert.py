import os
from PIL import Image
import pillow_heif
import argparse

def process_folder(input_folder: str, output_folder: str, size=(252, 252)):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        src_path = os.path.join(input_folder, filename)
        if not os.path.isfile(src_path):
            continue
        try:
            save_format = None
            name_lower = filename.lower()
            if name_lower.endswith(".heic"):
                heif_image = pillow_heif.open_heif(src_path)
                # Some versions expose .data as list; handle both
                data = heif_image.data[0] if hasattr(heif_image, "data") and isinstance(heif_image.data, (list, tuple)) else heif_image.data
                img = Image.frombytes(heif_image.mode, heif_image.size, data)
                filename = os.path.splitext(filename)[0] + ".jpg"
                save_format = "JPEG"
            elif name_lower.endswith((".jpg", ".jpeg", ".png")):
                img = Image.open(src_path)
                save_format = img.format or "JPEG"
            else:
                continue

            img_resized = img.resize(size)
            out_path = os.path.join(output_folder, filename)
            img_resized.save(out_path, format=save_format)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("✅ All images resized!")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--img_size", nargs=2, type=int, default=[252, 252])
    args = ap.parse_args()
    process_folder(args.input, args.output, size=tuple(args.img_size))
