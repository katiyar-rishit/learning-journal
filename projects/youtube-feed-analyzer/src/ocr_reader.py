import os
import easyocr
import pandas as pd
from datetime import datetime


# path
FRAMES_FOLDER = "data/raw_frames"
OUTPUT_FOLDER = "data/ocr_outputs"
BASE_NAME = "raw_ocr_output.csv"


# ensure output folder exists
def ensure_folders():
    os.makedirs("data/ocr_outputs", exist_ok=True)
    os.makedirs("data/raw_frames", exist_ok=True)


# auto-rename if file already exists
def get_unique_output_path(base_name):
    base_path = os.path.join(OUTPUT_FOLDER, base_name)

    if not os.path.exists(base_path):
        return base_path

    # if file exists, append number at end
    name, ext = os.path.splittext(base_name)
    count = 1

    while True:
        new_name = f"{name}_{count}{ext}"
        new_path = os.path.join(OUTPUT_FOLDER, new_name)

        if not os.path.exists(new_path):
            return new_path

        count += 1


OUTPUT_CSV = get_unique_output_path(BASE_NAME)


def extract_ocr_from_frames(
    frames_folder="data/raw_frames", output_name="raw_ocr_output.csv"
):
    ensure_folders()

    reader = easyocr.Reader(["en", "ja"], gpu=False)
    output_csv = get_unique_output_path(output_name)

    results = []

    for filename in sorted(os.listdir(frames_folder)):
        if filename.lower().endswith((".jpg", ".png")):
            path = os.path.join(frames_folder, filename)

            text_blocks = reader.readtext(path, detail=0)
            combined_text = " ".join(text_blocks)

            printf(f"Processed {filename}: {combined_text[:80]}...")

            results.append({"frame": filename, "raw_text": combined_text})

    df = pd.DataFrame(result)
    df.to_csv(output_csv, index=False)

    print("\n OCR extraction complete")
    print("Saved results to {output_csv}")

    return output_csv
