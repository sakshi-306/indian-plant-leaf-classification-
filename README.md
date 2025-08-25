<<<<<<< HEAD
# Indian Plant Leaf Classification using CNN 🌿

This repository implements a CNN to classify Indian plant leaves (species/disease categories) using TensorFlow/Keras.

## 📦 What’s inside
```
indian-plant-leaf-cnn/
├── notebooks/
│   └── Indian_Plant_Leaves_Classification.ipynb
├── src/
│   ├── resize_and_convert.py     # HEIC→JPG & resize to 252x252
│   ├── augment_images.py         # Albumentations pipeline (generates more images)
│   ├── rename_and_move.py        # Renames files to numeric sequence
│   ├── normalize_images.py       # Normalizes/resizes and saves
│   ├── train.py                  # Builds, trains, saves model + class_names.json
│   └── predict.py                # Loads model and predicts a single image
├── models/                       # Saved models (.h5)
├── requirements.txt
├── .gitignore
└── LICENSE
```

## 🗂️ Expected dataset layout
Place your data like this (one subfolder per class):
```
datasets/
├── Mango/
├── Guava/
├── Banana/
├── Neem/
└── Tulsi/
```

## 🚀 Setup
```bash
python -m venv .venv && source .venv/bin/activate  # (or .venv\Scripts\activate on Windows)
pip install -r requirements.txt
```

## 🧪 Train
```bash
python src/train.py --data_dir ./datasets --epochs 30 --img_size 252 252 --batch_size 32
```
This saves `models/plant_identifier.h5` and `models/class_names.json`.

## 🔍 Predict
```bash
python src/predict.py --model models/plant_identifier.h5 --classes models/class_names.json --image path/to/leaf.jpg --img_size 252 252
```

## 🛠️ Preprocessing utilities
- **HEIC/JPG resize**:
  ```bash
  python src/resize_and_convert.py --input /path/to/raw --output /path/to/resized
  ```
- **Augment images**:
  ```bash
  python src/augment_images.py --input /path/to/resized --output /path/to/aug --count 10
  ```
- **Rename sequentially**:
  ```bash
  python src/rename_and_move.py --input /path/to/aug --output /path/to/renamed
  ```
- **Normalize & save**:
  ```bash
  python src/normalize_images.py --input /path/to/renamed --output ./datasets/Mango
  ```
