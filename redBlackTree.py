class RedBlackTreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None
        self.color = 'RED'  # New nodes are always red initially

class RedBlackTree:
    def __init__(self):
        self.TNULL = RedBlackTreeNode(0)  # Sentinel node, acts as NIL
        self.TNULL.color = 'BLACK'  # The sentinel node is always black
        self.root = self.TNULL

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
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

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
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

    def fix_insert(self, k):
        while k.parent.color == 'RED':
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == 'RED':
                    u.color = 'BLACK'
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.rotate_left(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self.rotate_right(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == 'RED':
                    u.color = 'BLACK'
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rotate_right(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self.rotate_left(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'BLACK'

    def insert(self, key):
        node = RedBlackTreeNode(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 'RED'

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 'BLACK'
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def inorder_helper(self, node):
        if node != self.TNULL:
            self.inorder_helper(node.left)
            print(node.data, end=" ")
            self.inorder_helper(node.right)

    def inorder(self):
        self.inorder_helper(self.root)

    def search(self, key):
        node = self.root
        while node != self.TNULL:
            if key == node.data:
                return node
            elif key < node.data:
                node = node.left
            else:
                node = node.right
        return None  # Return None if the node is not found

    def rb_transplant(self, u, v):
        """Helper function to replace one subtree with another."""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_fix(self, x):
        """Fixing the Red-Black Tree after deletion."""
        while x != self.root and x.color == 'BLACK':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'RED':
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.rotate_left(x.parent)
                    w = x.parent.right

                if w.left.color == 'BLACK' and w.right.color == 'BLACK':
                    w.color = 'RED'
                    x = x.parent
                else:
                    if w.right.color == 'BLACK':
                        w.left.color = 'BLACK'
                        w.color = 'RED'
                        self.rotate_right(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = 'BLACK'
                    w.right.color = 'BLACK'
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'RED':
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.rotate_right(x.parent)
                    w = x.parent.left

                if w.right.color == 'BLACK' and w.left.color == 'BLACK':
                    w.color = 'RED'
                    x = x.parent
                else:
                    if w.left.color == 'BLACK':
                        w.right.color = 'BLACK'
                        w.color = 'RED'
                        self.rotate_left(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = 'BLACK'
                    w.left.color = 'BLACK'
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = 'BLACK'

    def delete(self, key):
        node = self.root
        while node != self.TNULL:
            if key == node.data:
                break
            elif key < node.data:
                node = node.left
            else:
                node = node.right

        if node == self.TNULL:
            print("Key not found")
            return

        y = node
        y_original_color = y.color
        if node.left == self.TNULL:
            x = node.right
            self.rb_transplant(node, node.right)
        elif node.right == self.TNULL:
            x = node.left
            self.rb_transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.rb_transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_original_color == 'BLACK':
            self.delete_fix(x)

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node
# Example usage
rbt = RedBlackTree()
rbt.insert(10)
rbt.insert(20)
rbt.insert(30)
rbt.insert(15)

# Inorder Traversal
print("Inorder before deletion:")
rbt.inorder()
print()

# Delete a node
rbt.delete(20)

# Inorder Traversal after deletion
print("Inorder after deletion:")
rbt.inorder()
print()

# Search for a node
result = rbt.search(15)
if result != None:
    print(f"Node found: {result.data}")
else:
    print("Node not found.")
