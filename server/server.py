from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from contact_tree import ContactTree

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Initialize the contact tree
contact_tree = ContactTree()

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = contact_tree.in_order_traversal()
    return jsonify(contacts)

@app.route('/contacts', methods=['POST'])
def add_contact():
    new_contact = request.get_json()
    contact_tree.insert(new_contact)  # Insert the contact into the tree
    return jsonify(new_contact), 201

@app.route('/contacts/<string:name>', methods=['PUT'])
def update_contact(name):
    contact = contact_tree.find(name)
    if contact is None:
        return jsonify({'message': 'Contact not found'}), 404

    # Update contact information
    data = request.get_json()
    contact.update(data)
    return jsonify(contact)



@app.route('/contacts/<string:name>', methods=['DELETE'])
def delete_contact(name):
    contact_tree.delete(name)
    return jsonify({'message': 'Contact deleted'})

if __name__ == '__main__':
    app.run(debug=True)
