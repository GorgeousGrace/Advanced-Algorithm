"""
References:
1. Wikipedia: Red–black tree — https://en.wikipedia.org/wiki/Red–black_tree
2. GeeksforGeeks: Various articles on BST and self-balancing trees
"""

RED = True
BLACK = False

class RBNode:
    """
    A node in the Red-Black Tree.

    Attributes:
        key: The key stored in this node.
        color: RED (True) or BLACK (False).
        left, right, parent: Child and parent references.
    """
    def __init__(self, key, color=RED, left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

class RBTree:
    """
    A Red-Black Tree implementation supporting insertion, search, and deletion.
    """

    def __init__(self):
        """
        Initialize an empty RBTree with a sentinel NIL node (BLACK).
        """
        self.NIL = RBNode(key=None, color=BLACK)
        self.root = self.NIL

    def insert(self, key):
        """
        Insert a 'key' into the Red-Black Tree.

        Steps:
        1. Perform a standard BST insert.
        2. Assign the new node color = RED.
        3. Call _fix_insert to restore Red-Black invariants if violated.
        """
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
            # Tree is empty, new_node becomes root
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # If new_node is now the root
        if new_node.parent is None:
            new_node.color = BLACK
            return

        # If grandparent doesn't exist, no need to fix
        if new_node.parent.parent is None:
            return
        
        # 2. Fix potential Red-Black violations
        self._fix_insert(new_node)

    def _fix_insert(self, node):
        """
        Restore Red-Black properties after inserting 'node'.
        Cases:
            1. Uncle is RED -> recolor parent, uncle, grandparent
            2. Uncle is BLACK + node is inside child (LR or RL) -> rotate
            3. Uncle is BLACK + node is outside child (LL or RR) -> rotate & recolor
        """
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
                    # Case 2 or 3
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._right_rotate(node.parent.parent)
            else:
                # Mirror cases if parent is a right child
                uncle = node.parent.parent.left
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
        """
        Left-rotate around node x.
        x becomes left child of its right child y.
        """
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
        """
        Right-rotate around node x.
        x becomes right child of its left child y.
        """
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
        """
        Return True if 'key' is found in the tree, else False.
        """
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
        """
        Delete the node with the given 'key' if it exists in the RBTree.

        Steps:
        1. BST find the node (z).
        2. If not found (z == NIL), do nothing.
        3. Perform standard BST deletion but track the original color.
        4. If original color was BLACK, call _fix_delete to restore invariants.
        """
        self._delete_helper(self.root, key)

    def _delete_helper(self, node, key):
        """
        Finds the node with 'key' and deletes it, then calls _fix_delete if needed.
        """
        z = self.NIL
        # 1. BST search to locate node z
        while node != self.NIL:
            if node.key == key:
                z = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if z == self.NIL:
            # Key not found
            return

        # y is the node we'll actually remove or move
        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            # Find successor (minimum of z.right)
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
            # Copy color of z into successor to preserve black-height
            y.color = z.color

        if y_original_color == BLACK:
            self._fix_delete(x)

    def _rb_transplant(self, u, v):
        """
        Replace subtree rooted at u with subtree rooted at v.
        """
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _fix_delete(self, x):
        """
        Restore Red-Black invariants after a delete operation
        potentially removed a BLACK node (or replaced it).
        """
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                sib = x.parent.right
                # Case 1: sibling is RED
                if sib.color == RED:
                    sib.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    sib = x.parent.right
                # Case 2: sibling is BLACK, both children black
                if sib.left.color == BLACK and sib.right.color == BLACK:
                    sib.color = RED
                    x = x.parent
                else:
                    # Case 3: sibling is black, left child is red, right child is black
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
                # Mirror logic if x is a right child
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
        """
        Return the node with the smallest key in the subtree rooted at 'node'.
        """
        while node.left != self.NIL:
            node = node.left
        return node
