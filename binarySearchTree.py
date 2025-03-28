class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key


class BST:
    def __init__(self):
        self.root = None

    # Insert function to insert a new node with the key
    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.value:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursive(node.right, key)

    # Search function to find a node with a specific key
    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.value == key:
            return node
        if key < node.value:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    # Inorder traversal (left, root, right)
    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    # Delete function to remove a node with the specific key
    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        # Base case
        if node is None:
            return node

        if key < node.value:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.value:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children
            min_value_node = self._min_value_node(node.right)
            node.value = min_value_node.value
            node.right = self._delete_recursive(node.right, min_value_node.value)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current


# Example of usage:
bst = BST()
bst.insert(10)
bst.insert(20)
bst.insert(5)
bst.insert(15)
bst.insert(30)

# Search for a value
print(bst.search(15))  # Should return the node with value 15

# Inorder Traversal
print(bst.inorder())  # Should return [5, 10, 15, 20, 30]

# Deleting a node
bst.delete(20)
print(bst.inorder())  # Should return [5, 10, 15, 30]
