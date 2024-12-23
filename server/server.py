from flask import Flask, request, jsonify
from flask_cors import CORS 
from contact_tree import ContactTree
import uuid  

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})


contact_tree = ContactTree()

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = contact_tree.in_order_traversal()
    return jsonify(contacts)




@app.route('/contacts', methods=['POST'])
def add_contact():
    new_contact = request.get_json()
    contact_tree.insert(new_contact)
    return jsonify(new_contact), 201




@app.route('/contacts/<contact_id>', methods=['PUT'])
def update_contact(contact_id):
    try:
        
        contact = contact_tree.find_by_id(contact_id) 
        if not contact:
            return jsonify({'message': 'Contact not found'}), 404
        

        data = request.get_json()
        contact.update(data)  

        return jsonify(contact), 200 
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Failed to update contact'}), 500



@app.route('/contacts/<string:name>', methods=['DELETE'])
def delete_contact(name):
    contact_tree.delete(name)
    return jsonify({'message': 'Contact deleted'})

if __name__ == '__main__':
    app.run(debug=True)
