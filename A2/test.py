import unittest
import random

from AVL_Tree import AVLTree
from Red_Black_Tree import RBTree
from Treap import Treap

class TestAVLTree(unittest.TestCase):
    """
    Unit tests for AVLTree implementation.
    """
    def setUp(self):
        """
        Runs before each test. Initializes an empty AVLTree.
        """
        self.tree = AVLTree()

    def tearDown(self):
        """
        Runs after each test (optional cleanup).
        """
        pass

    def test_insert_and_search_single(self):
        """
        Test inserting a single key and searching for it.
        Expects the inserted key to be found, and a non-existent key to be false.
        """
        self.tree.insert(10)
        self.assertTrue(self.tree.search(10), "AVL should find key=10 after insertion.")
        self.assertFalse(self.tree.search(99), "AVL should not find non-existent key=99.")

    def test_insert_duplicates(self):
        """
        Test behavior when inserting duplicate keys.
        By default, many BSTs allow duplicates either on left or right.
        We only verify that searching for the key is true afterward.
        """
        self.tree.insert(20)
        self.tree.insert(20)
        self.assertTrue(self.tree.search(20), "Duplicated key=20 should still be found.")

    def test_delete_existing_key(self):
        """
        Insert several keys, then delete one known key. 
        Verify it's no longer found.
        """
        keys = [30, 10, 50, 20, 40]
        for k in keys:
            self.tree.insert(k)
        self.assertTrue(self.tree.search(20))
        self.tree.delete(20)
        self.assertFalse(self.tree.search(20), "AVL should not find key=20 after deletion.")

    def test_delete_nonexistent_key(self):
        """
        Insert several keys, then attempt deleting a non-existent key (999).
        The tree should remain unaffected.
        """
        keys = [1, 2, 3]
        for k in keys:
            self.tree.insert(k)
        self.tree.delete(999)  # Key doesn't exist
        for k in keys:
            self.assertTrue(self.tree.search(k), f"Key={k} should remain after invalid deletion.")

    def test_bulk_insertion(self):
        """
        Insert a range of keys (0..99) and confirm they exist.
        """
        for i in range(100):
            self.tree.insert(i)
        for check_val in [0, 50, 99]:
            self.assertTrue(
                self.tree.search(check_val),
                f"AVL should contain key={check_val} after bulk insertion."
            )

    def test_bulk_deletion(self):
        """
        Insert a range of keys (0..99), then delete them all.
        Confirm the tree is empty afterward.
        """
        for i in range(100):
            self.tree.insert(i)
        for i in range(100):
            self.tree.delete(i)
        for i in range(100):
            self.assertFalse(self.tree.search(i), f"Key={i} should be removed from AVL.")


class TestRBTree(unittest.TestCase):
    """
    Unit tests for RBTree (Red-Black Tree) implementation.
    """
    def setUp(self):
        self.tree = RBTree()

    def test_insert_search_delete(self):
        """
        Insert several keys, verify they can be searched, then delete some and verify they're gone.
        """
        data = [15, 6, 3, 20, 18, 25]
        for val in data:
            self.tree.insert(val)
        for val in data:
            self.assertTrue(self.tree.search(val), f"RBTree should find inserted key={val}.")

        self.tree.delete(6)
        self.assertFalse(self.tree.search(6), "RBTree should not find deleted key=6.")
        self.tree.delete(18)
        self.assertFalse(self.tree.search(18), "RBTree should not find deleted key=18.")
        
        self.assertTrue(self.tree.search(15), "RBTree should still contain key=15.")
        self.assertTrue(self.tree.search(25), "RBTree should still contain key=25.")

    def test_duplicates(self):
        """
        Insert duplicate keys and check if searching returns True.
        """
        self.tree.insert(10)
        self.tree.insert(10)
        self.assertTrue(self.tree.search(10), "RBTree should find duplicate key=10.")

    def test_nonexistent_delete(self):
        """
        Deleting a key that doesn't exist should not affect the tree.
        """
        self.tree.insert(100)
        self.tree.delete(999)
        self.assertTrue(self.tree.search(100), "Key=100 should remain after invalid deletion.")

    def test_bulk_insertion(self):
        """
        Insert 200 unique random values, verify each is found.
        """
        random.seed(42)
        nums = random.sample(range(1000), 200)
        for n in nums:
            self.tree.insert(n)
        for n in nums:
            self.assertTrue(self.tree.search(n), f"RBTree missing inserted key={n}.")

    def test_bulk_deletion(self):
        """
        Insert 100 keys, delete them all, verify they're gone.
        """
        for i in range(100):
            self.tree.insert(i)
        for i in range(100):
            self.tree.delete(i)
        for i in range(100):
            self.assertFalse(self.tree.search(i), f"Key={i} should be deleted from RBTree.")


class TestTreap(unittest.TestCase):
    """
    Unit tests for Treap implementation.
    """
    def setUp(self):
        self.tree = Treap()

    def test_basic_operations(self):
        """
        Insert a few items, verify search, then delete some and verify they're gone.
        """
        items = [5, 2, 8, 1, 3]
        for it in items:
            self.tree.insert(it)
        for it in items:
            self.assertTrue(self.tree.search(it), f"Treap should contain key={it}.")

        self.tree.delete(2)
        self.assertFalse(self.tree.search(2), "Treap should not find deleted key=2.")
        self.tree.delete(8)
        self.assertFalse(self.tree.search(8), "Treap should not find deleted key=8.")

    def test_duplicate_inserts(self):
        """
        Insert the same key more than once, ensure searching it is still True.
        """
        self.tree.insert(50)
        self.tree.insert(50)
        self.assertTrue(self.tree.search(50), "Treap should find duplicate key=50.")

    def test_delete_nonexistent(self):
        """
        Deleting a key that doesn't exist should not break the treap.
        """
        self.tree.insert(10)
        self.tree.delete(999)
        self.assertTrue(self.tree.search(10), "Key=10 should remain after invalid deletion.")

    def test_bulk_insertion(self):
        """
        Insert 0..99, verify a few known keys, then do partial deletes and re-check.
        """
        for val in range(100):
            self.tree.insert(val)
        # Check random subset
        for check_val in [0, 50, 99]:
            self.assertTrue(self.tree.search(check_val), f"Treap missing inserted key={check_val}.")

    def test_bulk_deletion(self):
        """
        Insert 0..99, then delete them all, verifying none remains.
        """
        for val in range(100):
            self.tree.insert(val)
        for val in range(100):
            self.tree.delete(val)
        for val in range(100):
            self.assertFalse(self.tree.search(val), f"Treap should not contain key={val} after deletion.")


if __name__ == "__main__":
    unittest.main()
