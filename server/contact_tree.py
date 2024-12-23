import uuid

class ContactNode:
    def __init__(self, contact):
        self.contact = contact  # Store contact information (name, phone, email, etc.)
        self.left = None  # Left child
        self.right = None  # Right child
        self.height = 1  # Height of the node for AVL balancing

class ContactTree:
    def __init__(self):
        self.root = None

    def insert(self, contact):
        """Insert a contact into the AVL tree."""
        contact["id"] = str(uuid.uuid4())  # Assign a unique ID to the contact
        self.root = self._insert_recursive(self.root, contact)

    def _insert_recursive(self, node, contact):
        if not node:
            return ContactNode(contact)

        if contact["name"].lower() < node.contact["name"].lower():
            node.left = self._insert_recursive(node.left, contact)
        else:
            node.right = self._insert_recursive(node.right, contact)

        # Update the height of the node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Check balance and adjust if needed
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and contact["name"].lower() < node.left.contact["name"].lower():
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and contact["name"].lower() > node.right.contact["name"].lower():
            return self._rotate_left(node)

        # Left Right Case
        if balance > 1 and contact["name"].lower() > node.left.contact["name"].lower():
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left Case
        if balance < -1 and contact["name"].lower() < node.right.contact["name"].lower():
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def find_by_id(self, id):
        """Find a contact by its unique ID."""
        return self._find_by_id_recursive(self.root, id)

    def _find_by_id_recursive(self, node, id):
        if node is None:
            return None
        if node.contact["id"] == id:
            return node.contact
        left_result = self._find_by_id_recursive(node.left, id)
        if left_result:
            return left_result
        return self._find_by_id_recursive(node.right, id)

    def delete(self, name):
        """Delete a contact by name."""
        self.root = self._delete_recursive(self.root, name)

    def _delete_recursive(self, node, name):
        if not node:
            return node

        if name.lower() < node.contact["name"].lower():
            node.left = self._delete_recursive(node.left, name)
        elif name.lower() > node.contact["name"].lower():
            node.right = self._delete_recursive(node.right, name)
        else:
            # Node to be deleted found
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Node with two children: Get the inorder successor
            temp = self._min_value_node(node.right)
            node.contact = temp.contact
            node.right = self._delete_recursive(node.right, temp.contact["name"])

        # Update the height of the node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Check balance and adjust if needed
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _rotate_left(self, z):
        """Perform a left rotation."""
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_right(self, z):
        """Perform a right rotation."""
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _min_value_node(self, node):
        """Get the node with the smallest value (in-order successor)."""
        current = node
        while current.left:
            current = current.left
        return current

    def in_order_traversal(self):
        """Perform in-order traversal to get contacts sorted by name."""
        contacts = []
        self._in_order_recursive(self.root, contacts)
        return contacts

    def _in_order_recursive(self, node, contacts):
        if node:
            self._in_order_recursive(node.left, contacts)
            contacts.append(node.contact)
            self._in_order_recursive(node.right, contacts)
