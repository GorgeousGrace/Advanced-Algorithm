"""
References:
1. Wikipedia: AVL Tree — https://en.wikipedia.org/wiki/AVL_tree
2. GeeksforGeeks: Various articles on BST and self-balancing trees
"""

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Used to track balance factor

def get_height(node):
    """
    Return the height of the given node.
    If node is None, returns 0.
    """
    if not node:
        return 0
    return node.height

def get_balance(node):
    """
    Compute and return the balance factor of the given node:
    (height(left subtree) - height(right subtree)).
    """
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

def right_rotate(z):
    """
    Right-rotate around node z and return the new root of that subtree.
    """
    y = z.left
    T3 = y.right
    
    # Perform rotation
    y.right = z
    z.left = T3
    
    # Update heights
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    
    # y becomes the new root
    return y

def left_rotate(z):
    """
    Left-rotate around node z and return the new root of that subtree.
    """
    y = z.right
    T2 = y.left
    
    y.left = z
    z.right = T2
    
    # Update heights
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    
    return y

class AVLTree:
    """
    An AVL (self-balancing) Binary Search Tree implementation.
    """
    def __init__(self):
        self.root = None

    def insert(self, key):
        """
        Insert 'key' into the AVL Tree and rebalance if needed.
        """
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        # Normal BST insertion
        if not node:
            return AVLNode(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        
        # Update height of this ancestor node
        node.height = 1 + max(get_height(node.left), get_height(node.right))
        
        # Get the balance factor
        balance = get_balance(node)
        
        # If the node is unbalanced, then try out the 4 rotation cases:

        # Case 1: Left Left
        if balance > 1 and key < node.left.key:
            return right_rotate(node)
        
        # Case 2: Right Right
        if balance < -1 and key > node.right.key:
            return left_rotate(node)
        
        # Case 3: Left Right
        if balance > 1 and key > node.left.key:
            node.left = left_rotate(node.left)
            return right_rotate(node)
        
        # Case 4: Right Left
        if balance < -1 and key < node.right.key:
            node.right = right_rotate(node.right)
            return left_rotate(node)
        
        return node

    def search(self, key):
        """
        Return True if 'key' exists in the AVL Tree, False otherwise.
        """
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

    def delete(self, key):
        """
        Delete 'key' from the AVL Tree if it exists.
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """
        Internal recursive method to delete 'key' from subtree rooted at 'node'.
        Returns the new subtree root after deletion and rebalancing.
        """
        if not node:
            return node

        # 1) Perform BST delete
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node found
            if not node.left:
                # If left child is None, replace node with right child
                return node.right
            elif not node.right:
                # If right child is None, replace node with left child
                return node.left
            else:
                # Node with two children: replace with inorder successor
                temp = self._min_value_node(node.right)
                node.key = temp.key
                node.right = self._delete(node.right, temp.key)

        # If the tree had only one node, simply return
        if not node:
            return node

        # 2) Update height of current node
        node.height = 1 + max(get_height(node.left), get_height(node.right))
        
        # 3) Get the balance factor and rebalance if needed
        balance = get_balance(node)

        # Left Left
        if balance > 1 and get_balance(node.left) >= 0:
            return right_rotate(node)

        # Left Right
        if balance > 1 and get_balance(node.left) < 0:
            node.left = left_rotate(node.left)
            return right_rotate(node)

        # Right Right
        if balance < -1 and get_balance(node.right) <= 0:
            return left_rotate(node)

        # Right Left
        if balance < -1 and get_balance(node.right) > 0:
            node.right = right_rotate(node.right)
            return left_rotate(node)

        return node

    def _min_value_node(self, node):
        """
        Helper method to find the node with the smallest key in a subtree (used for inorder successor).
        """
        current = node
        while current.left:
            current = current.left
        return current
