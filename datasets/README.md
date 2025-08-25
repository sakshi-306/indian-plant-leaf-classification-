# 🌿 Dataset Setup for Indian Plant Leaf Classification

This project uses images of Indian plant leaves (e.g., Mango, Guava, Banana, Neem, Tulsi).  
Each class should be stored in its own folder inside the `datasets/` directory.

---

## 📂 Required Folder Structure
```
datasets/
├── Mango/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Guava/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Banana/
├── Neem/
└── Tulsi/
```

- Each subfolder = one class label.  
- Images should be **252x252 pixels** (use preprocessing scripts in `src/`).  
- Images can be `.jpg`, `.jpeg`, or `.png`.  

---

## 📥 Option 1: Use Your Own Dataset
- Collect leaf images and arrange them as shown above.  
- Use `src/resize_and_convert.py`, `src/augment_images.py`, etc., to preprocess them.  

---

## 📥 Option 2: Download a Public Dataset
You can use the **PlantVillage dataset** as a starting point:  
👉 [PlantVillage on Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease)  

After downloading:
- Extract the dataset  
- Keep only the plant classes you need  
- Rename folders (e.g., `Mango`, `Guava`, etc.)  

---

## 📥 Option 3: Download Sample Dataset (For Testing)
To quickly test the pipeline with a small dataset:  
```bash
python datasets/download_dataset.py
```

This will download and extract a **tiny sample dataset** into the `datasets/` folder.  
(It’s only for testing, not for serious training!)

---

## ⚠️ Note
- The full dataset is **not included in this repo** due to size limits.  
- Do **not** upload your dataset to GitHub. Keep it locally.
