from collections import UserDict
import re
import pickle
from datetime import datetime, timedelta
from notes import Notebook
from Levenshtein import distance as levenshtein_distance
from abc import ABC, abstractmethod

class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_notes(self, notes):
        pass

    @abstractmethod
    def display_commands(self, commands):
        pass

class ConsoleUI(UserInterface):
    def display_contacts(self, contacts):
        print("=== Contacts ===")
        for contact in contacts:
            print(f"{contact.name} - (contact.email) - {contact.phone}")

    def display_notes(self, notes):
        print("=== Notes===")
        for note in notes:
            print(note)

    def display_commands(self, commands):
        print("=== Commands ===")
        for command in commands:
            print(command)

    def get_user_input(self):
        return input("Enter you command: ")

class Field:
    """Base class for entry fields."""
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        pattern = re.compile(r"^\d{9}$")
        return pattern.match(value) is not None

class Email(Field):
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Invalid email address")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(value) is not None

class Birthday(Field):
    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError("Invalid birthday date")
        super().__init__(value)

    @staticmethod
    def validate_birthday(value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

class Address(Field):
    def __init__(self, street, city, postal_code, country):
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
        super().__init__(value=f"{street}, {city}, {postal_code}, {country}")

class Record:
    def __init__(self, name: Name, birthday: Birthday = None):
        self.id = None  # The ID will be assigned by AddressBook
        self.name = name
        self.phones = []
        self.emails = []
        self.birthday = birthday
        self.address = None  # Add a new property to store the address

    def add_address(self, address: Address):
        """Adds an address."""
        self.address = address

    def add_phone(self, phone: Phone):
        """Adds a phone number."""
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        """Removes a phone number."""
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        """Changes a phone number."""
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_email(self, email: Email):
        """Adds an email address."""
        self.emails.append(email)

    def remove_email(self, email: Email):
        """Removes an email address."""
        self.emails.remove(email)

    def edit_email(self, old_email: Email, new_email: Email):
        """Changes an email address."""
        self.remove_email(old_email)
        self.add_email(new_email)

    def edit_name(self, new_name: Name):
        """Changes the first and last name."""
        self.name = new_name

    class Record:
        def days_to_birthday(self):
            """Returns the number of days to the next birthday."""
            if not self.birthday or not self.birthday.value:
                return "No birth date provided"
            today = datetime.now()
            bday = datetime.strptime(self.birthday.value, "%Y-%m-%d")
            next_birthday = bday.replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days

    def __str__(self):
        """Returns a string representation of the entry, including the ID."""
        phones = ', '.join(phone.value for phone in self.phones)
        emails = ', '.join(email.value for email in self.emails)
        birthday_str = f", Birthday: {self.birthday.value}" if self.birthday else ""
        days_to_bday_str = f", Days until birthday: {self.days_to_birthday()}" if self.birthday else ""
        address_str = f"\nAddress: {self.address.value}" if self.address else ""
        return f"ID: {self.id}, Name: {self.name.value}, " \
               f"Phones: {phones}, Email: {emails}{birthday_str}{days_to_bday_str}{address_str}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.next_id = 1
        self.free_ids = set()

    def add_record(self, record: Record):
        """Adds an entry to the address book with ID management."""
        while self.next_id in self.data or self.next_id in self.free_ids:
            self.next_id += 1
        if self.free_ids:
            record.id = min(self.free_ids)
            self.free_ids.remove(record.id)
        else:
            record.id = self.next_id
            self.next_id += 1
        self.data[record.id] = record
        print(f"Added entry with ID: {record.id}.")

    def delete_record_by_id(self):
        """Deletes a record based on ID."""
        user_input = input("Enter the ID of the record you want to delete: ").strip()
        record_id_str = user_input.replace("ID: ", "").strip()

        try:
            record_id = int(record_id_str)
            if record_id in self.data:
                del self.data[record_id]
                self.free_ids.add(record_id)
                print(f"Deleted record with ID: {record_id}.")
            else:
                print("No record found with the provided ID.")
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def find_record(self, search_term):
        """Finds entries containing the exact phrase provided."""
        found_records = []
        for record in self.data.values():
            if search_term.lower() in record.name.value.lower():
                found_records.append(record)
                continue
            for phone in record.phones:
                if search_term in phone.value:
                    found_records.append(record)
                    break
            for email in record.emails:
                if search_term in email.value:
                    found_records.append(record)
                    break
        return found_records

    def find_records_by_name(self, name):
        """Finds records that match the given name and surname."""
        matching_records = []
        for record_id, record in self.data.items():
            if name.lower() in record.name.value.lower():
                matching_records.append((record_id, record))
        return matching_records

    def delete_record(self):
        """Deletes the record based on the selected ID after searching by name."""
        name_to_delete = input("Enter the name of the person you want to delete: ")
        matching_records = self.find_records_by_name(name_to_delete)

        if not matching_records:
            print("No matching records found.")
            return

        print("Found the following matching records:")
        for record_id, record in matching_records:
            print(f"ID: {record_id}, Record: {record}")

        try:
            record_id_to_delete = int(input("Enter the ID of the record you want to delete: "))
            if record_id_to_delete in self.data:
                del self.data[record_id_to_delete]
                self.free_ids.add(record_id_to_delete)  # Add the ID back to the free ID pool
                print(f"Deleted record with ID: {record_id_to_delete}.")
            else:
                print("No record found with the provided ID.")
        except ValueError:
            print("Invalid ID. Please enter a number.")


    def show_all_records(self):
        """Displays all entries in the address book."""
        if not self.data:
            print("The address book is empty.")    
            return
        for name, record in self.data.items():
            print(record)

    def __iter__(self):
        """Returns an iterator over the address book records."""
        self.current = 0
        return self

    def __next__(self):
        if self.current < len(self.data):
            records = list(self.data.values())[self.current:self.current+5]
            self.current += 5
            return records
        else:
            raise StopIteration


def suggest_correction_name(name_to_edit, matching_records):
    closest_name = min(matching_records, key=lambda x: levenshtein_distance(name_to_edit, x[1].name.value))
    return closest_name[1].name.value

def edit_record(book):
    """Edits an existing record in the address book."""
    name_to_edit = input("Enter the name you want to edit: ")
    matching_records = book.find_records_by_name(name_to_edit)

    if not matching_records:
        print("No matching records found.")
        return

    if len(matching_records) > 1:
        print("Found more than one matching record. Please choose one from the following:")
        for idx, (record_id, record) in enumerate(matching_records, start=1):
            print(f"{idx}. ID: {record_id}, Record: {record}")

        try:
            choice_idx = int(input("Enter the record number to edit: "))
            if 0 < choice_idx <= len(matching_records):
                record_id, record = matching_records[choice_idx - 1]
            else:
                print("Invalid record number.")
                return
        except ValueError:
            print("Invalid value. Enter a number.")
            return
    else:
        record_id, record = matching_records[0]

    print(f"Editing: ID: {record_id}, {name_to_edit}.")

    # Suggest corrections for name
    closest_name = suggest_correction_name(name_to_edit, matching_records)
    print(f"Did you mean: {closest_name} - for the name?")

    new_name_input = input("Enter the new name (press Enter to keep the current one): ")
    if new_name_input.strip():
        record.edit_name(Name(new_name_input))
        print("Updated name.")

    # Edit phone numbers
    if record.phones:
        print("Current phone numbers: ")
        for idx, phone in enumerate(record.phones, start=1):
            print(f"{idx}. {phone.value}")
        phone_to_edit = input("Enter the phone number to edit (press Enter to keep the current one): ")
        if phone_to_edit.strip():
            try:
                idx = int(phone_to_edit) - 1
                if 0 <= idx < len(record.phones):
                    new_phone_number = input("Enter the new phone number: ")
                    record.edit_phone(record.phones[idx], Phone(new_phone_number))
                    print("Phone number updated.")
                else:
                    print("Invalid phone number index.")
            except ValueError:
                print("Invalid value. Enter a number.")
    else:
        print("No phone numbers to edit.")

    # Edit email addresses
    if record.emails:
        print("Current email addresses: ")
        for idx, email in enumerate(record.emails, start=1):
            print(f"{idx}. {email.value}")
        email_to_edit = input("Enter the email address to edit (press Enter to keep the current one): ")
        if email_to_edit.strip():
            try:
                idx = int(email_to_edit) - 1
                if 0 <= idx < len(record.emails):
                    new_email = input("Enter the new email address: ")
                    record.edit_email(record.emails[idx], Email(new_email))
                    print("Email address updated.")
                else:
                    print("Invalid email address index.")
            except ValueError:
                print("Invalid value. Enter a number.")
    else:
        print("No email addresses to edit.")

    # Edit email addresses
    if record.emails:
        print("Current email addresses: ")
    for idx, email in enumerate(record.emails, start=1):
        print(f"{idx}. {email.value}")
    email_to_edit = input("Enter the email address to edit (press Enter to keep the current one): ")
    if email_to_edit.strip():
        try:
            idx = int(email_to_edit) - 1
            if 0 <= idx < len(record.emails):
                new_email = input("Enter the new email address: ")
                record.edit_email(record.emails[idx], Email(new_email))
                print("Email address updated.")
            else:
                print("Invalid email address index.")
        except ValueError:
            print("Invalid value. Enter a number.")
    else:
        print("No email addresses to edit.")

def save_address_book(book, filename='address_book.pkl'):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(book.data, file)
        print("Saved the address book.")
    except Exception as e:
        print(f"Error saving the address book: {e}")

def load_address_book(filename='address_book.pkl'):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        book = AddressBook()
        book.data = data
        print("Restored the address book.")
        return book
    except FileNotFoundError:
        print("File does not exist, creating a new address book.")
        return AddressBook()
    except Exception as e:
        print(f"Error loading the address book: {e}")
        return AddressBook()

def input_phone():
    """Asks the user to enter a phone number."""
    while True:
        try:
            number = input("Enter the phone number in the format '123456789' (press Enter to skip): ")
            if not number:
                return None
            return Phone(number)
        except ValueError as e:
            print(e)

def input_email():
    """Asks the user to enter an email address."""
    while True:
        try:
            address = input("Enter the email address (press Enter to skip): ")
            if not address:
                return None
            return Email(address)
        except ValueError as e:
            print(e)


def create_record():
    """Creates an entry in the address book based on user input."""
    name_input = input("Enter first and last name: ")
    name = Name(name_input)

    birthday = None
    while True:
        birthday_input = input("Enter the birthday (YYYY-MM-DD) or press Enter to skip: ")
        if not birthday_input:
            break
        try:
            birthday = Birthday(birthday_input)
            break
        except ValueError as e:
            print(e)

    record = Record(name, birthday)

    while True:
        try:
            phone_input = input("Enter phone number (or press Enter to finish adding phone numbers): ")
            if not phone_input:
                break
            phone = Phone(phone_input)
            record.add_phone(phone)
        except ValueError as e:
            print(e)

    while True:
        try:
            email_input = input("Enter email address (or press Enter to finish adding email addresses): ")
            if not email_input:
                break
            email = Email(email_input)
            record.add_email(email)
        except ValueError as e:
            print(e)

    # New functionality: Adding an address
    add_address = input("Do you want to add an address? (y/n): ").lower().strip()
    if add_address in ['y']:
        street = input("Enter street: ")
        city = input("Enter city: ")
        postal_code = input("Enter postal code: ")
        country = input("Enter country name: ")
        address = Address(street, city, postal_code, country)
        record.add_address(address)

    return record

def suggest_correction(contact_action, available_commands):
   # Levenshtein distance dla action
    closest_command = min(available_commands, key=lambda x: levenshtein_distance(contact_action, x))
    return closest_command


def suggest_correction_search(search_term, book):
    #Levenshtein distance dla search_term
    all_search_terms = [record.name.value for record in book.data.values()] + [phone.value for record in
                                                                               book.data.values() for phone in
                                                                               record.phones] + [email.value for record
                                                                                                 in book.data.values()
                                                                                                 for email in
                                                                                                 record.emails]

    closest_search_term = min(all_search_terms, key=lambda x: weighted_levenshtein_distance(search_term, x))
    return closest_search_term


def weighted_levenshtein_distance(s1, s2):
    len_s1 = len(s1)
    len_s2 = len(s2)

    if len_s1 == 0:
        return len_s2
    if len_s2 == 0:
        return len_s1

    matrix = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        matrix[i][0] = i

    for j in range(len_s2 + 1):
        matrix[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)

    # Weighted Levenshtein distance
    return matrix[len_s1][len_s2] / max(len_s1, len_s2)

def main():
    notebook = Notebook()
    notebook.load_notes()
    book = load_address_book()
    available_commands = ['add', 'search', 'delete', 'edit', 'show', 'exit']

    while True:
        action = input("Choose action: \nManage Contacts (c), Manage Notes (n), or Exit (e): ")

        if action == 'c':
            while True:
                contact_action = input(
                    "Choose action: \nAdd contact (a), Find contact (f), "
                    "Delete contact (d), Edit contact (e), Show all (s), Back (b): ")

                if contact_action == 'a':
                    record = create_record()
                    book.add_record(record)
                    print("Contact added.")
                elif contact_action == 'f':
                    search_term = input("Enter the search term: ")
                    found = book.find_record(search_term)
                    for record in found:
                        print(record)
                    if search_term not in found:
                        closest_search_term = suggest_correction_search(search_term, book)
                        print(f"Did you mean: {closest_search_term}   - for the search term?")
                elif contact_action == 'd':
                    book.delete_record_by_id()
                    print("Contact deleted.")
                elif contact_action == 'e':
                    edit_record(book)
                    print("Contact updated.")
                elif contact_action == 's':
                    book.show_all_records()
                elif contact_action == 'b':
                    break
                else:
                    closest_command = suggest_correction(contact_action, available_commands)
                    print(f"Did you mean: {closest_command}   - for the command?")
        elif action == 'n':
            while True:
                note_action = input(
                    "Choose action for notes: \nAdd note (a), Show notes (s), "
                    "Delete note (d), Back (b): ")

                if note_action == 'a':
                    title = input("Enter the title of the note: ")
                    content = input("Enter the content of the note: ")
                    notebook.add_note(title, content)
                    print("Note added.")
                elif note_action == 's':
                    notebook.show_notes()
                elif note_action == 'd':
                    note_id = input("Enter the ID of the note to delete: ")
                    notebook.delete_note(note_id)
                    print("Note deleted.")
                elif note_action == 'b':
                    break
                else:
                    print("Unknown action, please try again.")
        elif action == 'e':
            print("Exiting the program.")
            break
        else:
            print("Unknown action, please try again.")

    save_address_book(book)
    notebook.save_notes()

if __name__ == "__main__":
    notebook = Notebook()
    notebook.load_notes()
    book = load_address_book()
    ui = ConsoleUI()

    available_commands = ['add', 'search', 'delete', 'edit', 'show', 'exit']

    while True:
        action = input("Choose action: \nManage Contacts (c), Manage Notes (n), or Exit (e): ")

        if action == 'c':
            while True:
                contact_action = ui.get_user_input("Choose action: \nAdd contact (a), Find contact (f), "
                                                  "Delete contact (d), Edit contact (e), Show all (s), Back (b): ")
                # ... (continue with the logic for managing contacts)

        elif action == 'n':
            while True:
                note_action = ui.get_user_input(
                    "Choose action for notes: \nAdd note (a), Show notes (s), Delete note (d), Back (b): ")
                # ... (continue with the logic for managing notes)

        elif action == 'e':
            print("Exiting the program.")
            break

        else:
            print("Unknown action, please try again.")

    save_address_book(book)
    notebook.save_notes()