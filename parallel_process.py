import os
import time
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont
import zipfile

def extract_dataset(zip_path, extract_to):
    if zipfile.is_zipfile(zip_path):
        print("Extracting dataset...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("Dataset extracted successfully.")

def process_image(input_path, output_path):
    try:
        img = Image.open(input_path)
        img = img.resize((128, 128))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "Watermark", fill=(255, 255, 255))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_in_parallel(num_workers):
    input_dir = "data_set"
    output_dir = f"output_parallel_{num_workers}"

    image_paths = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".png", ".jpeg")):
                inp = os.path.join(root, file)
                out = os.path.join(output_dir, os.path.relpath(inp, input_dir))
                image_paths.append((inp, out))

    if not image_paths:
        print(f"No images found in {input_dir}.")
        return 0

    start_time = time.time()
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        executor.map(lambda p: process_image(*p), image_paths)
    end_time = time.time()

    return end_time - start_time

if __name__ == "__main__":
    zip_path = "data_set.zip"
    extract_to = "."

    if os.path.exists(zip_path):
        extract_dataset(zip_path, extract_to)

    workers_list = [1, 2, 4, 8]
    times = []

    print("\nWorkers | Time (s) | Speedup")
    print("--------|----------|--------")

    for workers in workers_list:
        exec_time = process_in_parallel(workers)
        if exec_time == 0:
            break
        times.append(exec_time)
        speedup = times[0] / exec_time
        print(f"{workers:<8}| {exec_time:.2f}     | {speedup:.2f}x")

    print("\nParallel Processing Completed")

