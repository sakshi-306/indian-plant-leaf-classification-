import os
import shutil
import argparse

def rename_and_move_files(input_folder: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    files = sorted(os.listdir(input_folder))
    files = [f for f in files if os.path.isfile(os.path.join(input_folder, f))]
    for index, filename in enumerate(files, start=1):
        ext = os.path.splitext(filename)[1]
        new_filename = f"{index}{ext}"
        src = os.path.join(input_folder, filename)
        dst = os.path.join(output_folder, new_filename)
        shutil.copy2(src, dst)
    print("Files renamed and moved successfully.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    rename_and_move_files(args.input, args.output)
