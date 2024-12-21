import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { ContactsComponent } from './contacts/contacts.component';
import { ContactService } from './contact.service';

@NgModule({
  declarations: [AppComponent, ContactsComponent],
  imports: [BrowserModule, AppRoutingModule, FormsModule, [HttpClientModule]],
  providers: [ContactService],
  bootstrap: [AppComponent],
})
export class AppModule {}
