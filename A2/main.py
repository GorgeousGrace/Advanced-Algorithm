"""
main.py

Compare insertion, search, and deletion times for AVL, Red-Black, and Treap.
Allows scaling up (e.g., 100k, 500k, 1M).
Generates random data to avoid near-ideal collisions or easy patterns.

Also creates plots for insertion, search, and deletion times using matplotlib,
so you can include them in your report.

Running Instructions:
    python main.py

Ensure you have matplotlib installed:
    pip install matplotlib
"""

import time
import random
import sys
import matplotlib.pyplot as plt

from AVL_Tree import AVLTree
from Red_Black_Tree import RBTree
from Treap import Treap

def generate_random_data(n=100000, seed=42):
    """
    Generates 'n' random integers in [0, 10^9], using 'seed' for reproducibility.
    This avoids purely sequential data, giving a more realistic distribution.
    """
    random.seed(seed)
    return [random.randint(0, 10**9) for _ in range(n)]

def benchmark_insertion(tree_class, data):
    """
    Creates a new 'tree_class' instance and inserts all items in 'data'.
    Returns the total time in seconds.
    """
    tree = tree_class()
    start = time.perf_counter()
    for val in data:
        tree.insert(val)
    end = time.perf_counter()
    return end - start

def benchmark_search(tree_class, data, queries):
    """
    Creates a new 'tree_class' instance, inserts 'data', then searches for each item in 'queries'.
    Returns (elapsed_time, found_count).
    """
    tree = tree_class()
    for val in data:
        tree.insert(val)
    start = time.perf_counter()
    found_count = 0
    for q in queries:
        if tree.search(q):
            found_count += 1
    end = time.perf_counter()
    return (end - start, found_count)

def benchmark_deletion(tree_class, data, del_keys):
    """
    Creates a new 'tree_class' instance, inserts 'data', then deletes each item in 'del_keys'.
    Returns the total time in seconds to perform all deletions.

    Note: If 'del_keys' contains elements not in 'data', the tree's delete method
    should simply handle them gracefully (often no-op).
    """
    tree = tree_class()
    for val in data:
        tree.insert(val)
    start = time.perf_counter()
    for d in del_keys:
        tree.delete(d)
    end = time.perf_counter()
    return end - start

def main():
    # You can adjust these sizes for your scaling tests
    sizes = [100000, 500000, 1000000]

    # We'll store all results for plotting
    avl_insert_times, rb_insert_times, treap_insert_times = [], [], []
    avl_search_times, rb_search_times, treap_search_times = [], [], []
    avl_delete_times, rb_delete_times, treap_delete_times = [], [], []

    # For curiosity: track how many keys are actually found by each DS in search
    avl_found_counts, rb_found_counts, treap_found_counts = [], [], []

    for s in sizes:
        print(f"\n=== Data size: {s} ===")

        # 1) Generate main data
        data = generate_random_data(n=s, seed=123)

        # 2) Prepare queries for searching:
        #    half from 'data' (expected found), half random new (expected not found)
        query_count = min(20000, s)  # or any fraction
        existing_part = random.sample(data, query_count // 2)
        new_part = generate_random_data(n=query_count // 2, seed=999)
        queries = existing_part + new_part
        random.shuffle(queries)

        # 3) Prepare deletion list: let's delete half of the data (existing) and half random new
        #    You can tweak the fraction as you like
        delete_count = min(20000, s)
        existing_del_part = random.sample(data, delete_count // 2)
        new_del_part = generate_random_data(n=delete_count // 2, seed=1234)
        del_keys = existing_del_part + new_del_part
        random.shuffle(del_keys)

        # ----------- Insertion -----------
        avl_insert_time = benchmark_insertion(AVLTree, data)
        rb_insert_time = benchmark_insertion(RBTree, data)
        treap_insert_time = benchmark_insertion(Treap, data)

        print("==== INSERTION TIMES ====")
        print(f"AVL:   {avl_insert_time:.4f}s")
        print(f"RB:    {rb_insert_time:.4f}s")
        print(f"Treap: {treap_insert_time:.4f}s")

        # ----------- Search -----------
        avl_search_time, avl_found = benchmark_search(AVLTree, data, queries)
        rb_search_time, rb_found = benchmark_search(RBTree, data, queries)
        treap_search_time, treap_found = benchmark_search(Treap, data, queries)

        print("\n==== SEARCH TIMES ====")
        print(f"AVL:   {avl_search_time:.4f}s, Found {avl_found}/{len(queries)}")
        print(f"RB:    {rb_search_time:.4f}s, Found {rb_found}/{len(queries)}")
        print(f"Treap: {treap_search_time:.4f}s, Found {treap_found}/{len(queries)}")

        # ----------- Deletion -----------
        avl_delete_time = benchmark_deletion(AVLTree, data, del_keys)
        rb_delete_time = benchmark_deletion(RBTree, data, del_keys)
        treap_delete_time = benchmark_deletion(Treap, data, del_keys)

        print("\n==== DELETION TIMES ====")
        print(f"AVL:   {avl_delete_time:.4f}s")
        print(f"RB:    {rb_delete_time:.4f}s")
        print(f"Treap: {treap_delete_time:.4f}s")

        # Store results
        avl_insert_times.append(avl_insert_time)
        rb_insert_times.append(rb_insert_time)
        treap_insert_times.append(treap_insert_time)

        avl_search_times.append(avl_search_time)
        rb_search_times.append(rb_search_time)
        treap_search_times.append(treap_search_time)

        avl_delete_times.append(avl_delete_time)
        rb_delete_times.append(rb_delete_time)
        treap_delete_times.append(treap_delete_time)

        avl_found_counts.append(avl_found)
        rb_found_counts.append(rb_found)
        treap_found_counts.append(treap_found)

    # ================= PLOTTING =================
    # We'll create three separate line plots: Insertion, Search, Deletion

    # 1) Insertion Time Plot
    plt.figure()
    plt.plot(sizes, avl_insert_times, label="AVL Insert")
    plt.plot(sizes, rb_insert_times, label="RB Insert")
    plt.plot(sizes, treap_insert_times, label="Treap Insert")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time (seconds)")
    plt.title("Insertion Time Comparison")
    plt.legend()
    plt.savefig("insertion_times.png")
    # plt.show()  # uncomment to display

    # 2) Search Time Plot
    plt.figure()
    plt.plot(sizes, avl_search_times, label="AVL Search")
    plt.plot(sizes, rb_search_times, label="RB Search")
    plt.plot(sizes, treap_search_times, label="Treap Search")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time (seconds)")
    plt.title("Search Time Comparison")
    plt.legend()
    plt.savefig("search_times.png")
    # plt.show()

    # 3) Deletion Time Plot
    plt.figure()
    plt.plot(sizes, avl_delete_times, label="AVL Delete")
    plt.plot(sizes, rb_delete_times, label="RB Delete")
    plt.plot(sizes, treap_delete_times, label="Treap Delete")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time (seconds)")
    plt.title("Deletion Time Comparison")
    plt.legend()
    plt.savefig("deletion_times.png")
    # plt.show()

    print("\nPlots saved as 'insertion_times.png', 'search_times.png', and 'deletion_times.png'.")

if __name__ == "__main__":
    main()
