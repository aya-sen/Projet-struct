# contact_tree.py

class ContactNode:
    def __init__(self, contact):
        self.contact = contact  # Stores the contact object (name, phone, email)
        self.left = None  # Left child
        self.right = None  # Right child

class ContactTree:
    def __init__(self):
        self.root = None

    def insert(self, contact):
        """Inserts a contact into the tree."""
        if not self.root:
            self.root = ContactNode(contact)
        else:
            self._insert_recursive(self.root, contact)

    def _insert_recursive(self, node, contact):
        """Helper method for recursively inserting into the tree."""
        if contact["name"].lower() < node.contact["name"].lower():
            if node.left:
                self._insert_recursive(node.left, contact)
            else:
                node.left = ContactNode(contact)
        else:
            if node.right:
                self._insert_recursive(node.right, contact)
            else:
                node.right = ContactNode(contact)

    def find(self, name):
        """Find a contact by name."""
        return self._find_recursive(self.root, name)

    def _find_recursive(self, node, name):
        """Helper method for recursively searching for a contact by name."""
        if node is None:
            return None
        if node.contact["name"].lower() == name.lower():
            return node.contact
        elif name.lower() < node.contact["name"].lower():
            return self._find_recursive(node.left, name)
        else:
            return self._find_recursive(node.right, name)

    def delete(self, name):
        """Delete a contact by name."""
        self.root = self._delete_recursive(self.root, name)

    def _delete_recursive(self, node, name):
        """Helper method for recursively deleting a contact."""
        if node is None:
            return node
        if name.lower() < node.contact["name"].lower():
            node.left = self._delete_recursive(node.left, name)
        elif name.lower() > node.contact["name"].lower():
            node.right = self._delete_recursive(node.right, name)
        else:
            # Node to be deleted found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node has two children
            temp = self._min_value_node(node.right)
            node.contact = temp.contact
            node.right = self._delete_recursive(node.right, temp.contact["name"])
        return node

    def _min_value_node(self, node):
        """Get the node with the minimum value in the tree."""
        current = node
        while current.left:
            current = current.left
        return current

    def in_order_traversal(self):
        """In-order traversal of the tree to get contacts in sorted order."""
        contacts = []
        self._in_order_recursive(self.root, contacts)
        return contacts

    def _in_order_recursive(self, node, contacts):
        """Helper method for in-order traversal."""
        if node:
            self._in_order_recursive(node.left, contacts)
            contacts.append(node.contact)
            self._in_order_recursive(node.right, contacts)
