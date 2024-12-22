from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from contact_tree import ContactTree
import uuid  

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})


# Initialize the contact tree
contact_tree = ContactTree()

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = contact_tree.in_order_traversal()
    return jsonify(contacts)

# @app.route('/contacts', methods=['POST'])
# def add_contact():
#     new_contact = request.get_json()
#     contact_tree.insert(new_contact)  # Insert the contact into the tree
#     return jsonify(new_contact), 201

@app.route('/contacts', methods=['POST'])
def add_contact():
    new_contact = request.get_json()
    new_contact["id"] = str(uuid.uuid4())  # Generate a unique ID
    contact_tree.insert(new_contact)
    return jsonify(new_contact), 201


# change name to id 
# @app.route('/contacts/<string:id>', methods=['PUT'])
# def update_contact(id):
#     contact = contact_tree.find(id)
#     if contact is None:
#         return jsonify({'message': 'Contact not found'}), 404

#     # Update contact information
#     data = request.get_json()
#     contact.update(data)
#     return jsonify(contact)

@app.route('/contacts/<contact_id>', methods=['PUT'])
def update_contact(contact_id):
    try:
        # Fetch the contact using the provided id
        contact = contact_tree.find_by_id(contact_id)  # Use find_by_id method to fetch contact
        if not contact:
            return jsonify({'message': 'Contact not found'}), 404
        
        # Update the contact data
        data = request.get_json()
        contact.update(data)  # Update contact attributes (name, phone, email)

        return jsonify(contact), 200  # Return the updated contact
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Failed to update contact'}), 500



@app.route('/contacts/<string:name>', methods=['DELETE'])
def delete_contact(name):
    contact_tree.delete(name)
    return jsonify({'message': 'Contact deleted'})

if __name__ == '__main__':
    app.run(debug=True)
