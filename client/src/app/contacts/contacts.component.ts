import { Component, OnInit } from '@angular/core';
import { ContactService } from '../contact.service'; // Import the service

interface Contact {
  id: string;
  name: string;
  phone: string;
  email: string;
}
@Component({
  selector: 'app-contacts',
  templateUrl: './contacts.component.html',
  styleUrls: ['./contacts.component.css'],
})
export class ContactsComponent implements OnInit {
  contacts: Contact[] = [];
  newContact: Contact = { id: '', name: '', phone: '', email: '' };
  selectedContact: Contact = { id: '', name: '', phone: '', email: '' };
  showAddForm: boolean = false;
  showEditForm: boolean = false;
  searchQuery: string = '';

  constructor(private contactService: ContactService) {}

  ngOnInit(): void {
    this.contactService.getContacts().subscribe(
      (data: Contact[]) => {
        this.contacts = data;
      },
      (error) => {
        console.error('Error fetching contacts:', error);
      }
    );
  }

  addContact() {
    this.newContact.id = this.newContact.id || this.generateUniqueId();

    this.contactService.addContact(this.newContact).subscribe(
      (contact: Contact) => {
        this.contacts.push(contact);

        this.newContact = { id: '', name: '', phone: '', email: '' };
        this.showAddForm = false;
      },
      (error) => {
        console.error('Error adding contact:', error);
      }
    );
  }

  generateUniqueId(): string {
    return '_' + Math.random().toString(36).substr(2, 9);
  }

  deleteContact(contact: any) {
    this.contactService.deleteContact(contact.name).subscribe(() => {
      this.contacts = this.contacts.filter((c) => c !== contact);
    });
  }

  editContact(contact: any) {
    this.selectedContact = { ...contact };
    this.showEditForm = true;
  }

  updateContact() {
    this.contactService
      .updateContact(this.selectedContact.id, this.selectedContact)
      .subscribe(
        (updatedContact: Contact) => {
          const index = this.contacts.findIndex(
            (c) => c.id === updatedContact.id
          );
          if (index !== -1) {
            this.contacts[index] = updatedContact;
          }
          this.showEditForm = false;
        },
        (error) => {
          console.error('Error updating contact:', error);
        }
      );
  }

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

  closeAddForm() {
    this.showAddForm = false;
  }

  closeEditForm() {
    this.showEditForm = false;
  }
}
