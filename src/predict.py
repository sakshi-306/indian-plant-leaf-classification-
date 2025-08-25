import argparse, json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

def load_class_names(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def predict(model_path, classes_path, img_path, img_size=(252,252)):
    model = tf.keras.models.load_model(model_path)
    class_names = load_class_names(classes_path)

    img = image.load_img(img_path, target_size=img_size)
    arr = image.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    preds = model.predict(arr)
    idx = int(np.argmax(preds[0]))
    conf = float(np.max(preds[0]))
    return {"class": class_names[idx], "confidence": conf, "index": idx}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--classes", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--img_size", nargs=2, type=int, default=[252, 252])
    args = ap.parse_args()
    out = predict(args.model, args.classes, args.image, tuple(args.img_size))
    print(f"Predicted: {out['class']} (confidence: {out['confidence']:.3f})")
