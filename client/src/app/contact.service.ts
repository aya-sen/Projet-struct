import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface Contact {
  name: string;
  phone: string;
  email: string;
}

@Injectable({
  providedIn: 'root',
})
export class ContactService {
  private apiUrl = 'http://127.0.0.1:5000/contacts'; // Flask API URL

  constructor(private http: HttpClient) {}

  // Get all contacts
  getContacts(): Observable<Contact[]> {
    return this.http.get<Contact[]>(this.apiUrl);
  }

  // Add a new contact
  addContact(contact: { name: string; phone: string; email: string }) {
    return this.http.post<{ name: string; phone: string; email: string }>(
      'http://localhost:5000/contacts',
      contact
    ); // Explicitly specify the return type here
  }

  // Update a contact
  updateContact(name: string, contact: Partial<Contact>): Observable<Contact> {
    return this.http.put<Contact>(`${this.apiUrl}/${name}`, contact);
  }

  // Delete a contact
  deleteContact(name: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${name}`);
  }
}
