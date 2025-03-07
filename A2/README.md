# Advanced Algorithm Projects

Welcome to the **Advanced-Algorithm** repository! This repo contains multiple assignments and projects related to advanced algorithms and data structures for the COSC 520 course.

## Repository Structure

```
Advanced-Algorithm/
├── A2/
│   ├── AVL_Tree.py
│   ├── Red_Black_Tree.py
│   ├── Treap.py
│   ├── main.py
│   └── (other code, test files, or dataset files)
├── (other assignment folders or files in the main branch)
└── README.md (this file)
```

---

## Running Instructions (Main Branch)

### 1. Cloning the Repository

```bash
git clone https://github.com/GorgeousGrace/Advanced-Algorithm.git
cd Advanced-Algorithm
```

### 2. Overview of Main Branch Contents

- **Assignment 1** or other code (if any) might reside at the top level.
- **Assignment 2** Contains code for comparing AVL Tree, Red-Black Tree, and Treap.


---

## Running Instructions for A2

Inside the **A2** folder, you’ll find:

- `AVL_Tree.py`, `Red_Black_Tree.py`, `Treap.py`  
  Each file implements a self-balancing data structure with methods for insert, search, and delete.  
- `main.py`  
  The main benchmarking script that:
  1. Generates random datasets
  2. Tests insertion, search, and deletion performance
  3. Produces plots (insertion_times.png, search_times.png, deletion_times.png)

**To run** the benchmarks:

1. **Navigate** to the A2 folder:
   ```bash
   cd A2
   ```

2. **Install** Python dependencies (if not installed already):
   ```bash
   pip install matplotlib
   ```
   (Everything else should be standard library.)

3. **Execute** the script:
   ```bash
   python main.py
   ```
   By default, `main.py` will:
   - Benchmark data sizes of 100k, 500k, and 1 million elements
   - Print timing results to the console
   - Generate three `.png` files showing performance (insertion, search, deletion).

4. **(Optional) Export the Dataset**  
   If you wish to store or share the generated dataset (1 million random integers), run:
   ```bash
   python main.py --export-dataset
   ```
   This command will create `my_dataset.txt` containing the randomly generated data. You can upload that file to a hosting service and include the link in your assignment PDF.

### File Overview (A2)

- **`AVL_Tree.py`**: AVL Tree class (insert, search, delete)  
- **`Red_Black_Tree.py`**: Red-Black Tree class (insert, search, delete)  
- **`Treap.py`**: Treap class (insert, search, delete, with randomized priorities)  
- **`main.py`**: Orchestrates data generation, benchmarking, and plotting.

---

## License / References

Include any license info or references here. For example:

- **License**: MIT (if applicable)
- **References**:
  - [Wikipedia: AVL Tree](https://en.wikipedia.org/wiki/AVL_tree)
  - [Wikipedia: Red–Black Tree](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)
  - [Wikipedia: Treap](https://en.wikipedia.org/wiki/Treap)
  - [GeeksforGeeks](https://www.geeksforgeeks.org/) for data structure tutorials.

---
