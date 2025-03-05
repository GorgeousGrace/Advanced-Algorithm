import unittest
import random


from AVL_Tree import AVLTree
from Red_Black_Tree import RBTree
from Treap import Treap

class TestAVLTree(unittest.TestCase):
    def setUp(self):
        """Runs before each test."""
        self.tree = AVLTree()

    def tearDown(self):
        """Runs after each test (optional cleanup)."""
        pass

    def test_insert_and_search_single(self):
        """Test inserting a single key and searching for it."""
        self.tree.insert(10)
        self.assertTrue(self.tree.search(10), "AVL should find key=10 after insertion.")
        self.assertFalse(self.tree.search(99), "AVL should not find a non-existent key=99.")

    def test_insert_duplicates(self):
        """Test behavior when inserting duplicate keys."""
        self.tree.insert(20)
        self.tree.insert(20)  # Depending on the implementation, duplicates may go to left/right
        # We only verify that searching for 20 is true
        self.assertTrue(self.tree.search(20))

    def test_delete_existing_key(self):
        """Test deleting a key that exists."""
        keys = [30, 10, 50, 20, 40]
        for k in keys:
            self.tree.insert(k)
        self.assertTrue(self.tree.search(20))
        self.tree.delete(20)
        self.assertFalse(self.tree.search(20), "AVL should not find deleted key=20.")

    def test_delete_nonexistent_key(self):
        """Test deleting a key that was never inserted."""
        keys = [1, 2, 3]
        for k in keys:
            self.tree.insert(k)
        self.tree.delete(999)  # Key doesn't exist
        # Just ensure it doesn't break the tree
        for k in keys:
            self.assertTrue(self.tree.search(k), f"Key={k} should still be in AVL.")

    def test_bulk_insertion(self):
        """Insert a larger range of keys and confirm they exist."""
        for i in range(100):
            self.tree.insert(i)
        # Check random subset
        for check_val in [10, 50, 99]:
            self.assertTrue(self.tree.search(check_val),
                            f"AVL should contain key={check_val} after bulk insertion.")

class TestRBTree(unittest.TestCase):
    def setUp(self):
        self.tree = RBTree()

    def test_insert_search_delete(self):
        """Simple end-to-end test of RBT."""
        data = [15, 6, 3, 20, 18, 25]
        for val in data:
            self.tree.insert(val)

        # Search for all inserted
        for val in data:
            self.assertTrue(self.tree.search(val),
                            f"RBTree should find inserted key={val}.")

        # Delete a couple
        self.tree.delete(6)
        self.assertFalse(self.tree.search(6), "RBTree should not find deleted key=6.")
        self.tree.delete(18)
        self.assertFalse(self.tree.search(18), "RBTree should not find deleted key=18.")
        
        # Ensure others are still present
        self.assertTrue(self.tree.search(15), "RBTree should still contain key=15.")
        self.assertTrue(self.tree.search(25), "RBTree should still contain key=25.")

    def test_duplicates(self):
        """Insert duplicate keys; check if search returns True."""
        self.tree.insert(10)
        self.tree.insert(10)
        self.assertTrue(self.tree.search(10), "RBTree should find 10 after duplicates inserted.")

    def test_nonexistent_delete(self):
        """Delete key that doesn't exist."""
        self.tree.insert(100)
        self.tree.delete(999)
        self.assertTrue(self.tree.search(100))

    def test_bulk_insertion(self):
        random.seed(42)
        nums = random.sample(range(1000), 200)  # 200 unique random numbers < 1000
        for n in nums:
            self.tree.insert(n)
        
        # Check that all are found
        for n in nums:
            self.assertTrue(self.tree.search(n), f"RBTree missing inserted key={n}.")

class TestTreap(unittest.TestCase):
    def setUp(self):
        self.tree = Treap()

    def test_basic_operations(self):
        """Insert a few items and verify search."""
        items = [5, 2, 8, 1, 3]
        for it in items:
            self.tree.insert(it)
        # Check search
        for it in items:
            self.assertTrue(self.tree.search(it),
                            f"Treap should contain inserted key={it}.")

        # Delete a couple
        self.tree.delete(2)
        self.assertFalse(self.tree.search(2), "Treap should not find deleted key=2.")
        self.tree.delete(8)
        self.assertFalse(self.tree.search(8), "Treap should not find deleted key=8.")

    def test_duplicate_inserts(self):
        self.tree.insert(50)
        self.tree.insert(50)  # Insert again
        self.assertTrue(self.tree.search(50))

    def test_delete_nonexistent(self):
        self.tree.insert(10)
        self.tree.delete(999)
        self.assertTrue(self.tree.search(10))

    def test_bulk_insertion(self):
        for val in range(100):
            self.tree.insert(val)
        # random checks
        self.assertTrue(self.tree.search(0))
        self.assertTrue(self.tree.search(50))
        self.assertTrue(self.tree.search(99))

 
if __name__ == "__main__":
    unittest.main()
