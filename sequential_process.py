import os
import time
from PIL import Image, ImageDraw, ImageFont
import zipfile

ZIP_FILE = "data_set.zip"
INPUT_DIR = "data_set"   
OUTPUT_DIR = "output_seq"

if not os.path.exists(INPUT_DIR) and os.path.exists(ZIP_FILE):
    print("Extracting dataset...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(".")
    print("Dataset extracted successfully!")


def add_watermark(image, text="© Fizzaa"):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()

 
    bbox = draw.textbbox((0, 0), text, font=font)
    textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]

    x = width - textwidth - 10
    y = height - textheight - 10

    draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))
    return image

def process_images():
    start_time = time.time()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    count = 0

    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                count += 1
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, INPUT_DIR)
                output_subfolder = os.path.join(OUTPUT_DIR, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)
                output_path = os.path.join(output_subfolder, file)

                try:
                    img = Image.open(input_path).convert("RGB")
                    img = img.resize((128, 128))
                    img = add_watermark(img)
                    img.save(output_path)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    end_time = time.time()
    print(f"\nSequential Processing Complete!")
    print(f"Processed {count} images.")
    print(f"Total Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    process_images()
