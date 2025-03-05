import random

class TreapNode:
    def __init__(self, key):
        self.key = key
        self.priority = random.random()  # or use random.randint(...) 
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return TreapNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
            # If heap property violated (child priority > parent)
            if node.left.priority > node.priority:
                node = self._right_rotate(node)
        else:
            node.right = self._insert(node.right, key)
            if node.right.priority > node.priority:
                node = self._left_rotate(node)
        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Found the node
            # If one child is None, replace node with that child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Rotate based on priority to move node down
                if node.left.priority > node.right.priority:
                    node = self._right_rotate(node)
                    node.right = self._delete(node.right, key)
                else:
                    node = self._left_rotate(node)
                    node.left = self._delete(node.left, key)
        return node

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y
