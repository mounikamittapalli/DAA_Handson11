class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key
        self.height = 1  # Height of a node starts as 1

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance_factor(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1

        # Return the new root
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1

        # Return the new root
        return y

    def insert(self, node, key):
        # 1. Perform the normal BST insert
        if node is None:
            return Node(key)

        if key < node.value:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        # 2. Update the height of this ancestor node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # 3. Get the balance factor to check whether this node became unbalanced
        balance_factor = self.get_balance_factor(node)

        # If the node becomes unbalanced, then there are 4 cases

        # Left Left Case
        if balance_factor > 1 and key < node.left.value:
            return self.right_rotate(node)

        # Right Right Case
        if balance_factor < -1 and key > node.right.value:
            return self.left_rotate(node)

        # Left Right Case
        if balance_factor > 1 and key > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance_factor < -1 and key < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        # Return the (unchanged) node pointer
        return node

    def insert_root(self, key):
        self.root = self.insert(self.root, key)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.value, end=" ")
            self.inorder(root.right)

    # Search Method
    def search(self, root, key):
        if root is None or root.value == key:
            return root
        elif key < root.value:
            return self.search(root.left, key)
        return self.search(root.right, key)

    # Delete Method
    def delete(self, root, key):
        # Step 1: Perform the standard BST delete
        if root is None:
            return root

        if key < root.value:
            root.left = self.delete(root.left, key)
        elif key > root.value:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.get_minimum(root.right)
            root.value = temp.value
            root.right = self.delete(root.right, temp.value)

        if root is None:
            return root

        root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1
        balance_factor = self.get_balance_factor(root)

        # Left Left Case
        if balance_factor > 1 and self.get_balance_factor(root.left) >= 0:
            return self.right_rotate(root)

        # Right Right Case
        if balance_factor < -1 and self.get_balance_factor(root.right) <= 0:
            return self.left_rotate(root)

        # Left Right Case
        if balance_factor > 1 and self.get_balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance_factor < -1 and self.get_balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_minimum(self, node):
        while node.left is not None:
            node = node.left
        return node
# Example usage
avl_tree = AVLTree()

# Inserting elements into AVL Tree
avl_tree.insert_root(10)
avl_tree.insert_root(20)
avl_tree.insert_root(30)
avl_tree.insert_root(15)
avl_tree.insert_root(25)

# Inorder traversal before deletion
print("Inorder traversal of the AVL Tree:")
avl_tree.inorder(avl_tree.root)
print()

# Search for a node
search_result = avl_tree.search(avl_tree.root, 15)
if search_result:
    print(f"Node with value {search_result.value} found.")
else:
    print("Node not found.")

# Delete a node
avl_tree.delete(avl_tree.root, 20)

# Inorder traversal after deletion
print("Inorder traversal of the AVL Tree after deletion:")
avl_tree.inorder(avl_tree.root)
print()
