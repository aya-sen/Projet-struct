import { Component } from '@angular/core';
import { ContactService } from '../contact.service'; // Import the service

@Component({
  selector: 'app-contacts',
  templateUrl: './contacts.component.html',
  styleUrls: ['./contacts.component.css'],
})
export class ContactsComponent {
  showAddForm: boolean = false;
  showEditForm: boolean = false;
  newContact: { name: string; phone: string; email: string } = {
    name: '',
    phone: '',
    email: '',
  };
  selectedContact: { name: string; phone: string; email: string } = {
    name: '',
    phone: '',
    email: '',
  };
  contacts: Array<{ name: string; phone: string; email: string }> = [];
  searchQuery: string = '';

  constructor(private contactService: ContactService) {}
  // Load contacts from backend
  ngOnInit(): void {
    this.contactService.getContacts().subscribe(
      (data) => {
        this.contacts = data;
      },
      (error) => {
        console.error('Error fetching contacts:', error);
      }
    );
  }

  // Add a new contact
  addContact() {
    console.log('Adding new contact:', this.newContact); // Add this log to see if the function is called
    if (
      this.newContact.name &&
      this.newContact.phone &&
      this.newContact.email
    ) {
      this.contactService
        .addContact(this.newContact)
        .subscribe(
          (contact: { name: string; phone: string; email: string }) => {
            this.contacts.push(contact); // Now TypeScript knows the contact has the correct type
            this.newContact = { name: '', phone: '', email: '' }; // Reset the form
            this.showAddForm = false; // Hide the form
          }
        );
    } else {
      console.log('Invalid form data'); // Add this log to check for empty data
    }
  }

  // Delete a contact
  deleteContact(contact: any) {
    this.contactService.deleteContact(contact.name).subscribe(() => {
      this.contacts = this.contacts.filter((c) => c !== contact); // Remove from frontend
    });
  }

  // Edit a contact: Pre-fill the form with the selected contact's details
  editContact(contact: any) {
    this.selectedContact = { ...contact };
    this.showEditForm = true;
  }

  // Update the contact
  updateContact() {
    console.log('Updating contact:', this.selectedContact); // Log for debugging
    this.contactService
      .updateContact(this.selectedContact.name, this.selectedContact)
      .subscribe(
        (updatedContact) => {
          const index = this.contacts.findIndex(
            (c) => c.name === updatedContact.name
          );
          if (index !== -1) {
            this.contacts[index] = updatedContact; // Update frontend with the updated contact
          }
          this.showEditForm = false; // Hide the edit form after success
        },
        (error) => {
          console.error('Error updating contact:', error); // Log error
        }
      );
  }

  // Filter contacts based on the search query
  filteredContacts() {
    if (!this.searchQuery) {
      return this.contacts;
    }
    return this.contacts.filter(
      (contact) =>
        contact.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        contact.phone.includes(this.searchQuery) ||
        contact.email.toLowerCase().includes(this.searchQuery.toLowerCase())
    );
  }

  // Close the "Add Contact" form
  closeAddForm() {
    this.showAddForm = false; // Hide the Add form
  }

  // Close the "Edit Contact" form
  closeEditForm() {
    this.showEditForm = false; // Hide the Edit form
  }
}
