import os
import cv2
from albumentations import (
    HorizontalFlip, VerticalFlip, RandomBrightnessContrast, Rotate, GaussianBlur, Compose, Resize
)
import argparse

def augment_folder(input_folder: str, output_folder: str, count_per_image: int = 10, size=(252,252)):
    os.makedirs(output_folder, exist_ok=True)
    aug = Compose([
        Resize(size[0], size[1]),
        HorizontalFlip(p=0.5),
        VerticalFlip(p=0.5),
        RandomBrightnessContrast(p=0.5),
        GaussianBlur(blur_limit=3, p=0.3),
    ])
    count = 0
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".heic")):
            continue
        img_path = os.path.join(input_folder, filename)
        image = cv2.imread(img_path)
        if image is None:
            print(f"Skipping unreadable: {filename}")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        stem = os.path.splitext(filename)[0]
        for i in range(count_per_image):
            augmented = aug(image=image)["image"]
            out = os.path.join(output_folder, f"{stem}_{i}.jpg")
            cv2.imwrite(out, cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR))
            count += 1
    print(f"Generated {count} augmented images. All Done ✅")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--count", type=int, default=10)
    ap.add_argument("--img_size", nargs=2, type=int, default=[252, 252])
    args = ap.parse_args()
    augment_folder(args.input, args.output, args.count, size=tuple(args.img_size))
