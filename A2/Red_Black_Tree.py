RED = True
BLACK = False

class RBNode:
    def __init__(self, key, color=RED, left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

class RBTree:
    def __init__(self):
        self.NIL = RBNode(key=None, color=BLACK)  # Sentinel leaf
        self.root = self.NIL

    def insert(self, key):
        """Insert key into the Red-Black Tree."""
        new_node = RBNode(key=key, color=RED, left=self.NIL, right=self.NIL)
        parent = None
        current = self.root

        # 1. BST insert to find position
        while current != self.NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if not parent:
            # Tree is empty
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # 2. If new root, color it black
        if not new_node.parent:
            new_node.color = BLACK
            return

        # 3. If grandparent doesn't exist, just return
        if not new_node.parent.parent:
            return
        
        # 4. Fix violations
        self._fix_insert(new_node)

    def _fix_insert(self, node):
        """Restore Red-Black properties after insertion."""
        while node.parent.color == RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                # Case 1: Uncle is red
                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    # Case 2: Uncle is black, node is right child
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    # Case 3: Uncle is black, node is left child
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                # Mirror cases
                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._left_rotate(node.parent.parent)
            
            if node == self.root:
                break
        self.root.color = BLACK

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def search(self, key):
        """Return True if key is found, else False."""
        return self._search_helper(self.root, key)

    def _search_helper(self, node, key):
        if node == self.NIL:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self._search_helper(node.left, key)
        else:
            return self._search_helper(node.right, key)

    def delete(self, key):
        """Delete a node with the given key if it exists."""
        self._delete_helper(self.root, key)

    def _delete_helper(self, node, key):
        # Standard BST search
        z = self.NIL
        while node != self.NIL:
            if node.key == key:
                z = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if z == self.NIL:
            # Key not found in the tree
            return

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            # Find successor
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        
        if y_original_color == BLACK:
            self._fix_delete(x)

    def _rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                sib = x.parent.right
                # Case 1: sibling is red
                if sib.color == RED:
                    sib.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    sib = x.parent.right
                # Case 2: sibling is black, children are black
                if sib.left.color == BLACK and sib.right.color == BLACK:
                    sib.color = RED
                    x = x.parent
                else:
                    # Case 3: sibling is black, left child is red
                    if sib.right.color == BLACK:
                        sib.left.color = BLACK
                        sib.color = RED
                        self._right_rotate(sib)
                        sib = x.parent.right
                    # Case 4: sibling is black, right child is red
                    sib.color = x.parent.color
                    x.parent.color = BLACK
                    sib.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                sib = x.parent.left
                if sib.color == RED:
                    sib.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    sib = x.parent.left
                if sib.right.color == BLACK and sib.left.color == BLACK:
                    sib.color = RED
                    x = x.parent
                else:
                    if sib.left.color == BLACK:
                        sib.right.color = BLACK
                        sib.color = RED
                        self._left_rotate(sib)
                        sib = x.parent.left
                    sib.color = x.parent.color
                    x.parent.color = BLACK
                    sib.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node
