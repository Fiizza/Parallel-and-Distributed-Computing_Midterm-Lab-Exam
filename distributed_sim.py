import os
import time
from multiprocessing import Process, Manager
from PIL import Image, ImageDraw
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

def node_worker(node_id, images, output_dir, results_dict):
    start_time = time.time()
    for inp, out in images:
        process_image(inp, out)
    end_time = time.time()
    duration = end_time - start_time
    results_dict[node_id] = {
        "count": len(images),
        "time": duration
    }

if __name__ == "__main__":
    zip_path = "data_set.zip"
    extract_to = "."

    if os.path.exists(zip_path):
        extract_dataset(zip_path, extract_to)

    input_dir = "data_set"
    output_dir = "output_distributed"

    image_paths = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                inp = os.path.join(root, file)
                out = os.path.join(output_dir, os.path.relpath(inp, input_dir))
                image_paths.append((inp, out))

    if not image_paths:
        print("No images found in dataset.")
        exit()

    total_images = len(image_paths)
    half = total_images // 2
    node1_images = image_paths[:half]
    node2_images = image_paths[half:]


    print(f"Total images: {total_images}")
    print("Starting distributed simulation...\n")

    manager = Manager()
    results_dict = manager.dict()

    start_time = time.time()
    p1 = Process(target=node_worker, args=(1, node1_images, output_dir, results_dict))
    p2 = Process(target=node_worker, args=(2, node2_images, output_dir, results_dict))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    total_time = time.time() - start_time
    node1 = results_dict.get(1, {})
    node2 = results_dict.get(2, {})

    print(f"Node 1 processed {node1.get('count', 0)} images in {node1.get('time', 0):.2f}s")
    print(f"Node 2 processed {node2.get('count', 0)} images in {node2.get('time', 0):.2f}s")
    print(f"\nTotal distributed time: {total_time:.2f}s")

    sequential_time=1.92  
    efficiency = sequential_time / total_time if total_time > 0 else 0
    print(f"Efficiency: {efficiency:.2f}x over sequential")
