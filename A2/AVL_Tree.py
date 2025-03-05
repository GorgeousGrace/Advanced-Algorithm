class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Needed to track balance

def get_height(node):
    if not node:
        return 0
    return node.height

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

def right_rotate(z):
    # Perform rotation
    y = z.left
    T3 = y.right
    
    # Rotate
    y.right = z
    z.left = T3
    
    # Update heights
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    
    # Return new root
    return y

def left_rotate(z):
    # Perform rotation
    y = z.right
    T2 = y.left
    
    # Rotate
    y.left = z
    z.right = T2
    
    # Update heights
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    
    # Return new root
    return y


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert key into the AVL Tree."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        # 1. Normal BST insertion
        if not node:
            return AVLNode(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        
        # 2. Update height
        node.height = 1 + max(get_height(node.left), get_height(node.right))
        
        # 3. Get balance factor
        balance = get_balance(node)
        
        # 4. Balance if needed
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
        """Return True if key is in the AVL Tree, False otherwise."""
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
        """Delete key from the AVL Tree if it exists."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        # BST delete
        if not node:
            return node
        elif key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node found
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Replace with inorder successor (smallest in right subtree)
                temp = self._min_value_node(node.right)
                node.key = temp.key
                node.right = self._delete(node.right, temp.key)

        # If the tree has only one node
        if not node:
            return node

        # Update height
        node.height = 1 + max(get_height(node.left), get_height(node.right))
        
        # Rebalance
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
        current = node
        while current.left:
            current = current.left
        return current
