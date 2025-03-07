"""
References:
1. Wikipedia: Treap — https://en.wikipedia.org/wiki/Treap
2. GeeksforGeeks: Various articles on BST and self-balancing trees
"""

import random

class TreapNode:
    """
    A node in the Treap.

    Attributes:
        key: The key stored at this node.
        priority: A random priority to maintain heap property.
        left: Reference to the left child.
        right: Reference to the right child.
    """
    def __init__(self, key):
        self.key = key
        # Use either random.random() for a float priority in [0,1]
        # or random.randint for an integer priority.
        self.priority = random.random()
        self.left = None
        self.right = None

class Treap:
    """
    Treap (Tree + Heap):
    - A binary search tree (BST) by 'key'.
    - A heap by 'priority' (children have strictly lower priority than the node).
    - Insertion, search, and deletion all average O(log n).
      Worst case can degrade to O(n), but this is rare.
    """

    def __init__(self):
        """
        Initialize an empty Treap.
        """
        self.root = None

    def search(self, key):
        """
        Check if 'key' exists in the Treap.

        Returns:
            bool: True if 'key' is found, False otherwise.
        """
        return self._search(self.root, key)

    def _search(self, node, key):
        """
        Internal recursive search.
        If node is None, the key doesn't exist.
        Otherwise, compare and go left/right based on BST property.
        """
        if not node:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def insert(self, key):
        """
        Insert a new 'key' into the Treap.

        Steps:
        1. Insert as in a normal BST (recursive).
        2. If child's priority is higher than parent's, rotate to fix violation.
        """
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """
        Internal recursive insertion:
        - Insert by BST rules.
        - If newly inserted node's priority > current node's priority, rotate.
        """
        if not node:
            return TreapNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
            # If heap property is violated (child has higher priority)
            if node.left.priority > node.priority:
                node = self._right_rotate(node)
        else:
            node.right = self._insert(node.right, key)
            if node.right.priority > node.priority:
                node = self._left_rotate(node)
        return node

    def delete(self, key):
        """
        Delete 'key' from the Treap if it exists.
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """
        Internal recursive deletion:
        - If key < node.key, recurse left.
        - If key > node.key, recurse right.
        - If key == node.key, remove this node:
            * If node has one child, return that child.
            * If node has two children, rotate based on priority to move the node down,
              then remove it when it has at most one child.
        """
        if not node:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Found the node to delete
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Rotate based on priority
                if node.left.priority > node.right.priority:
                    node = self._right_rotate(node)
                    node.right = self._delete(node.right, key)
                else:
                    node = self._left_rotate(node)
                    node.left = self._delete(node.left, key)
        return node

    def _left_rotate(self, x):
        """
        Left-rotate around node x:
         x                   y
          \                 / \
           y      -->      x   ...
          /
        ...
        """
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _right_rotate(self, x):
        """
        Right-rotate around node x:
            x            y
           /            / \
          y      -->  ...  x
           \
           ...
        """
        y = x.left
        x.left = y.right
        y.right = x
        return y
