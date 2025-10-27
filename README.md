# Image Preprocessing – Sequential, Parallel and Distributed Processing

Name: Fizzaa  
Roll No: SP23-BAI-023  

## Overview
This project implements three approaches for batch image preprocessing:
1. Sequential Processing  
2. Parallel Processing (Multiprocessing)  
3. Simulated Distributed Processing  

Each image is resized to 128x128, a watermark is added, and the processed images are saved in respective output folders.

---

## Task Summaries

### Task 1 – Sequential Processing
- Processes all images one by one.
- Saves results to the folder output_seq.
- Uses time.perf_counter() to measure total execution time.
- Run file: sequential_process.py

### Task 2 – Parallel Processing
- Uses Python’s multiprocessing.Pool to perform image processing in parallel.
- Tested with 2, 4, and 8 workers.
- Saves results to the folder output_parallel.
- Run file: parallel_process.py

### Task 3 – Simulated Distributed Processing
- Simulates two “nodes” using multiprocessing.Manager().
- Each node processes half of the dataset.
- The master process combines node times and calculates efficiency.
- Run file: distributed_process.py

---

## Performance Comparison

| Approach              | Description                     | Time (s) | Relative Speedup |
|------------------------|----------------------------------|----------|------------------|
| Sequential             | Single-threaded execution        | 1.09 s   | 1.00×            |
| Parallel (2 workers)   | Multiprocessing                  | 0.47 s   | 2.32×            |
| Parallel (4 workers)   | Multiprocessing                  | 0.61 s   | 1.78×            |
| Parallel (8 workers)   | Multiprocessing                  | 1.09 s   | 1.00×            |
| Distributed (2 nodes)  | Simulated 2-machine environment  | 1.53 s   | 0.71×            |

---

## Best Configuration

2 workers gave the fastest execution (around 2.3× faster than sequential).

Reasons:
- Uses both CPU cores efficiently.
- Keeps process communication overhead low.
- Avoids file I/O bottlenecks when writing many files at once.

---

## Discussion

Parallelism improved performance by processing multiple images at the same time using different CPU cores. Each process handled its own images independently, which reduced the overall runtime compared to sequential processing.  
However, speedup did not keep increasing after 2–4 workers because of disk I/O limitations and data transfer overhead between processes. The system reached its practical efficiency limit with 2 workers.  
Further improvement could be achieved with faster disk I/O or GPU-based parallelism.

---



## Author
Name: Fizzaa  
Roll No: SP23-BAI-023  
Collaborator: SP23-BAI-016  

---


