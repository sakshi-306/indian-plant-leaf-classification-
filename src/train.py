import os, json, argparse
import tensorflow as tf
from tensorflow import keras

def get_datasets(data_dir, img_size=(252,252), batch_size=32, seed=42):
    train_ds = keras.utils.image_dataset_from_directory(
        data_dir, shuffle=True, image_size=img_size, batch_size=batch_size,
        validation_split=0.2, subset="training", seed=seed
    )
    val_ds = keras.utils.image_dataset_from_directory(
        data_dir, shuffle=True, image_size=img_size, batch_size=batch_size,
        validation_split=0.2, subset="validation", seed=seed
    )
    AUTOTUNE = tf.data.AUTOTUNE
    return train_ds.prefetch(AUTOTUNE), val_ds.prefetch(AUTOTUNE), train_ds.class_names

def build_model(num_classes, img_size=(252,252)):
    data_augmentation = keras.Sequential([
        keras.layers.RandomFlip("horizontal"),
        keras.layers.RandomRotation(0.2),
        keras.layers.RandomZoom(0.2),
    ])
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=(img_size[0], img_size[1], 3)),
        data_augmentation,
        keras.layers.Conv2D(32, (3,3), activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D(2,2),
        keras.layers.Conv2D(64, (3,3), activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D(2,2),
        keras.layers.Conv2D(128, (3,3), activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D(2,2),
        keras.layers.Flatten(),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(num_classes, activation='softmax')
    ])
    opt = keras.optimizers.Adam(learning_rate=1e-4)
    model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def train(data_dir, img_w, img_h, batch_size, epochs, out_model):
    train_ds, val_ds, class_names = get_datasets(data_dir, (img_w, img_h), batch_size)
    model = build_model(num_classes=len(class_names), img_size=(img_w, img_h))

    early = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=[early])

    os.makedirs(os.path.dirname(out_model) or ".", exist_ok=True)
    model.save(out_model)

    # Save class names next to model
    classes_path = os.path.join(os.path.dirname(out_model) or ".", "class_names.json")
    with open(classes_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)
    print(f"Saved model to {out_model}")
    print(f"Saved class names to {classes_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True, help="Root folder with class subfolders")
    ap.add_argument("--img_size", nargs=2, type=int, default=[252, 252])
    ap.add_argument("--batch_size", type=int, default=32)
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--out_model", default="models/plant_identifier.h5")
    args = ap.parse_args()
    train(args.data_dir, args.img_size[0], args.img_size[1], args.batch_size, args.epochs, args.out_model)
