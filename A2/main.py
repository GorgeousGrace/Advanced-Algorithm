# main.py

import random
import time

from AVL_Tree import AVLTree
from Red_Black_Tree import RBTree
from Treap import Treap

def generate_data(n=100000, seed=42):
    """Generate a list of n random integers."""
    random.seed(seed)
    return [random.randint(0, 10**9) for _ in range(n)]

def benchmark_insertion(tree_class, data):
    """Insert all elements of 'data' into the given 'tree_class'."""
    tree = tree_class()
    start = time.perf_counter()
    for val in data:
        tree.insert(val)
    end = time.perf_counter()
    return end - start

def benchmark_search(tree_class, data, search_values):
    """Insert 'data' into tree, then search for each val in 'search_values'."""
    tree = tree_class()
    for val in data:
        tree.insert(val)

    start = time.perf_counter()
    found_count = 0
    for s_val in search_values:
        if tree.search(s_val):
            found_count += 1
    end = time.perf_counter()
    return end - start, found_count

if __name__ == "__main__":
    # Example sizes: adjust as needed for your testing
    sizes = [10000, 50000, 100000]

    print("Benchmarking AVL, Red-Black, and Treap...")

    for s in sizes:
        print(f"\n=== Data size: {s} ===")
        data = generate_data(s)
        
        # 1) Insertion times
        avl_insert_time = benchmark_insertion(AVLTree, data)
        rb_insert_time = benchmark_insertion(RBTree, data)
        treap_insert_time = benchmark_insertion(Treap, data)

        print(f"Insert - AVL: {avl_insert_time:.4f}s | RB: {rb_insert_time:.4f}s | Treap: {treap_insert_time:.4f}s")

        # 2) Search times (search a subset or random sample)
        # We'll sample up to 10% of 'data' for searching
        search_count = min(s // 10, 5000)  # or pick any search size
        search_vals = random.sample(data, search_count)
        
        avl_search_time, avl_found = benchmark_search(AVLTree, data, search_vals)
        rb_search_time, rb_found = benchmark_search(RBTree, data, search_vals)
        treap_search_time, treap_found = benchmark_search(Treap, data, search_vals)

        print(f"Search - AVL: {avl_search_time:.4f}s (found={avl_found}) | "
              f"RB: {rb_search_time:.4f}s (found={rb_found}) | "
              f"Treap: {treap_search_time:.4f}s (found={treap_found})")
