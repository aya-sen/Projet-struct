import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Contact {
  id: string;
  name: string;
  phone: string;
  email: string;
}

@Injectable({
  providedIn: 'root',
})
export class ContactService {
  private apiUrl = 'http://127.0.0.1:5000/contacts';

  constructor(private http: HttpClient) {}

  getContacts(): Observable<Contact[]> {
    return this.http.get<Contact[]>(this.apiUrl);
  }

  addContact(contact: Contact): Observable<Contact> {
    return this.http.post<Contact>('http://127.0.0.1:5000/contacts', contact); 
  }

  updateContact(contactId: string, updatedData: any): Observable<any> {
    const url = `http://127.0.0.1:5000/contacts/${contactId}`;
    return this.http.put(url, updatedData);
  }

  deleteContact(name: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${name}`);
  }
}
