from collections import UserDict
import re
import pickle
from datetime import datetime, timedelta
from notes import Notebook
from Levenshtein import distance as levenshtein_distance


class Field:
    """Base class for entry fields."""

    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Niepoprawny numer telefonu")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        pattern = re.compile(r"^\d{9}$")
        return pattern.match(value) is not None


class Email(Field):
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Niepoprawny adres email")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        pattern = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(value) is not None


class Birthday(Field):
    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError("Niepoprawna data urodzenia")
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

    def days_to_birthday(self):
        """Returns the number of days to the next birthday."""
        if not self.birthday or not self.birthday.value:
            return "Brak daty urodzenia"
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
        birthday_str = f", Urodziny: {self.birthday.value}" if self.birthday else ""
        days_to_bday_str = f", Dni do urodzin: {self.days_to_birthday()}" if self.birthday else ""
        address_str = f"\nAdres: {self.address.value}" if self.address else ""
        return (f"ID: {self.id}, Imię i nazwisko: {self.name.value}, "
                f"Telefony: {phones}, Email: {emails}"
                f"{birthday_str}{days_to_bday_str}{address_str}")


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.next_id = 1
        self.free_ids = set()

    def add_record(self, record: Record):
        """Dodaje wpis do książki adresowej z zarządzaniem ID."""
        record.id = self._get_next_record_id()
        self.data[record.id] = record
        print(f"Dodano wpis z ID: {record.id}.")

    def _get_next_record_id(self):
        """Pomocnicza metoda do uzyskania kolejnego ID."""
        while self.next_id in self.data or self.next_id in self.free_ids:
            self.next_id += 1
        return self.free_ids.pop() if self.free_ids else self.next_id

    def delete_record_by_id(self):
        """Deletes a record based on ID."""
        user_input = input("Podaj ID rekordu, który chcesz usunąć: ").strip()
        record_id_str = user_input.replace("ID: ", "").strip()

        try:
            record_id = int(record_id_str)
            if record_id in self.data:
                del self.data[record_id]
                self.free_ids.add(record_id)
                print(f"Usunięto rekord o ID: {record_id}.")
            else:
                print("Nie znaleziono rekordu o podanym ID.")
        except ValueError:
            print("Nieprawidłowe ID. Proszę podać liczbę.")

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
        name_to_delete = input(
            "Podaj imię i nazwisko osoby, którą chcesz usunąć: ")
        matching_records = self.find_records_by_name(name_to_delete)

        if not matching_records:
            print("Nie znaleziono pasujących rekordów.")
            return

        print("Znaleziono następujące pasujące rekordy:")
        for record_id, record in matching_records:
            print(f"ID: {record_id}, Rekord: {record}")

        try:
            record_id_to_delete = int(
                input("Podaj ID rekordu, który chcesz usunąć: "))
            if record_id_to_delete in self.data:
                del self.data[record_id_to_delete]
                # Add the ID back to the free ID pool
                self.free_ids.add(record_id_to_delete)
                print(f"Usunięto rekord o ID: {record_id_to_delete}.")
            else:
                print("Nie znaleziono rekordu o podanym ID.")
        except ValueError:
            print("Nieprawidłowe ID. Proszę podać liczbę.")

    def show_all_records(self):
        """Displays all entries in the address book."""
        if not self.data:
            print("Książka adresowa jest pusta.")
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

    def edit_record(self):
        """Edits a record based on the selected name."""
        name_to_edit = input("Podaj imię i nazwisko osoby, którą chcesz edytować: ")
        matching_records = self.find_records_by_name(name_to_edit)

        if not matching_records:
            print("Nie znaleziono pasujących rekordów.")
            return

        print("Znaleziono następujące pasujące rekordy:")
        for record_id, record in matching_records:
            print(f"ID: {record_id}, Rekord: {record}")

        record_id_to_edit_input = input("Podaj ID rekordu, który chcesz edytować: ")
        if record_id_to_edit_input.strip() == '':
            print("Anulowano edycję rekordu.")
            return

        try:
            record_id_to_edit = int(record_id_to_edit_input)
            if record_id_to_edit not in self.data:
                print("Nie znaleziono rekordu o podanym ID.")
                return
            record = self.data[record_id_to_edit]
        except ValueError:
            print("Nieprawidłowa wartość. Proszę podać liczbę.")
            return

        # Edycja imienia i nazwiska
        new_name_input = input('Podaj nowe imię i nazwisko (lub wciśnij Enter, aby pominąć): ')
        if new_name_input:
            record.name = Name(new_name_input)

        # Edycja numeru telefonu
        if record.phones:
            print("Obecne numery telefonów:")
            for idx, phone in enumerate(record.phones, 1):
                print(f"{idx}. {phone.value}")
            phone_choice = input("Wybierz numer do edycji (lub wciśnij Enter, aby pominąć): ")
            if phone_choice.isdigit():
                phone_index = int(phone_choice) - 1
                if 0 <= phone_index < len(record.phones):
                    new_phone_value = input("Podaj nowy numer telefonu: ")
                    if Phone.validate_phone(new_phone_value):
                        record.phones[phone_index] = Phone(new_phone_value)
                    else:
                        print("Niepoprawny format numeru telefonu.")
                else:
                    print("Nieprawidłowy wybór numeru telefonu.")
            else:
                print("Pominięto edycję numeru telefonu.")

        # Edycja adresu email
        if record.emails:
            # Wyświetlenie obecnych adresów email
            print("Obecne adresy email:")
            for idx, email in enumerate(record.emails, 1):
                print(f"{idx}. {email.value}")
            email_choice = input("Wybierz adres email do edycji (lub wciśnij Enter, aby pominąć): ")
            if email_choice.isdigit():
                email_index = int(email_choice) - 1
                if 0 <= email_index < len(record.emails):
                    new_email_value = input("Podaj nowy adres email: ")
                    if Email.validate_email(new_email_value):
                        record.emails[email_index] = Email(new_email_value)
                    else:
                        print("Niepoprawny format adresu email.")
                else:
                    print("Nieprawidłowy wybór adresu email.")
            else:
                print("Pominięto edycję adresu email.")

        new_birthday_input = input("Podaj nową datę urodzenia (YYYY-MM-DD) lub wciśnij Enter, aby pominąć: ")
        if new_birthday_input:
            if Birthday.validate_birthday(new_birthday_input):
                record.birthday = Birthday(new_birthday_input)
            else:
                print("Niepoprawny format daty urodzenia.")

        print("Wpis zaktualizowany.")


def save_address_book(book, filename='address_book.pkl'):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(book.data, file)
        print("Zapisano książkę adresową.")
    except Exception as e:
        print(f"Błąd przy zapisie książki adresowej: {e}")


def load_address_book(filename='address_book.pkl'):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            book = AddressBook()
            book.data = data
            print("Książka adresowa została wczytana.")
            return book
    except FileNotFoundError:
        print("Plik nie istnieje. Tworzenie nowej książki adresowej.")
        return AddressBook()
    except Exception as e:
        print(f"Nie udało się wczytać książki adresowej: {e}")
        return AddressBook()


def input_phone():
    """Asks the user to enter a phone number."""
    while True:
        try:
            number = input(
                "Podaj numer telefonu w formacie '123456789' (naciśnij Enter, aby pominąć): ")
            if not number:
                return None
            return Phone(number)
        except ValueError as e:
            print(e)


def input_email():
    """Asks the user to enter an email address."""
    while True:
        try:
            address = input(
                "Podaj adres email (naciśnij Enter, aby pominąć): ")
            if not address:
                return None
            return Email(address)
        except ValueError as e:
            print(e)


def create_record():
    """Creates an entry in the address book based on user input."""
    name_input = input("Podaj imię i nazwisko: ")
    name = Name(name_input)

    birthday = None
    while True:
        birthday_input = input(
            "Podaj datę urodzenia (YYYY-MM-DD) lub wciśnij Enter, aby pominąć: ")
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
            phone_input = input(
                "Podaj numer telefonu (lub wciśnij Enter, aby zakończyć dodawanie numerów): ")
            if not phone_input:
                break
            phone = Phone(phone_input)
            record.add_phone(phone)
        except ValueError as e:
            print(e)

    while True:
        try:
            email_input = input(
                "Podaj adres email (lub wciśnij Enter, aby zakończyć dodawanie adresów email): ")
            if not email_input:
                break
            email = Email(email_input)
            record.add_email(email)
        except ValueError as e:
            print(e)

    # New functionality: Adding an address
    add_address = input("Czy chcesz dodać adres? (t/n): ").lower().strip()
    if add_address in ['t']:
        street = input("Podaj ulicę: ")
        city = input("Podaj miasto: ")
        postal_code = input("Podaj kod pocztowy: ")
        country = input("Podaj nazwę państwa: ")
        address = Address(street, city, postal_code, country)
        record.add_address(address)

    return record


def suggest_closest_command(contact_action, available_commands):
    closest_command = min(available_commands, key=lambda x: abs(
        ord(x) - ord(contact_action)))
    return closest_command


def suggest_correction_search(search_term, book):
    # Levenshtein distance dla search_term
    all_search_terms = [record.name.value for record in book.data.values()] + [phone.value for record in
                                                                               book.data.values() for phone in
                                                                               record.phones] + [email.value for record
                                                                                                 in book.data.values()
                                                                                                 for email in
                                                                                                 record.emails]

    closest_search_term = min(
        all_search_terms, key=lambda x: weighted_levenshtein_distance(search_term, x))
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
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i]
                               [j - 1] + 1, matrix[i - 1][j - 1] + cost)

    # Weighted Levenshtein distance
    return matrix[len_s1][len_s2] / max(len_s1, len_s2)


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def main():
    notebook = Notebook()
    notebook.load_notes()
    book = load_address_book()
    available_commands = ['d', 'z', 'u', 'e', 'p', 'z']
    while True:
        action = input(
            "Wybierz akcję: \nZarządzaj Kontaktami (z), Zarządzaj notatkami (n), albo Wyjdź (q): ")
        if action == 'z':
            while True:
                contact_action = input(
                    "Wybierz działanie: \nDodaj kontakt (d), Znajdź kontakt (z), "
                    "Usuń kontakt (u), Edytuj kontakt (e), Pokaż wszystkie (p), Wróć (q): ")
                if contact_action == 'd':
                    record = create_record()
                    book.add_record(record)
                    print("Dodano kontakt.")
                elif contact_action == 'z':
                    search_term = input("Wpisz szukaną frazę: ")
                    found = book.find_record(search_term)
                    for record in found:
                        print(record)
                        continue
                    if search_term not in found:
                        closest_search_term = suggest_correction_search(
                            search_term, book)
                        print(f"Czy chodziło Ci o: {closest_search_term} - dla frazy wyszukiwania?")
                elif contact_action == 'u':
                    book.delete_record_by_id()
                    print("Usunięto kontakt.")
                elif contact_action == 'e':
                    book.edit_record()
                    print("Zaktualizowano kontakt.")
                elif contact_action == 'p':
                    book.show_all_records()
                elif contact_action == 'q':
                    break
                else:
                    closest_command = suggest_closest_command(
                        contact_action, available_commands)
                    # closest_search_term = suggest_correction_search(search, book)
                    print(f"Czy chodziło Ci o wybranie: {closest_command}   - dla komendy ")
        elif action == 'n':
            while True:
                note_action = input("Wybierz działanie dla notatek: \nDodaj notatkę (d), Pokaż notatki (p), "
                                    "Usuń notatkę (u), Edytuj notatkę (e), Wyszukaj notatki według tagu (t), "
                                    "Sortuj notatki według tagów (s), Wróć (q): ")
                if note_action == 'd':
                    title = input("Podaj tytuł notatki: ")
                    content = input("Podaj treść notatki: ")
                    tags = [tag.strip() for tag in input("Podaj tagi oddzielone przecinkami "
                                                         "(naciśnij Enter, aby pominąć): ").split(',')]
                    notebook.add_note(title, content, tags)
                    print("Dodano notatkę.")
                elif note_action == 'p':
                    notebook.show_notes()
                elif note_action == 'u':
                    note_id = input("Podaj ID notatki do usunięcia: ")
                    notebook.delete_note(int(note_id))
                    print("Usunięto notatkę.")
                elif note_action == 'e':
                    notebook.edit_note()
                    print("Zaktualizowano notatkę.")
                elif note_action == 't':
                    notebook.show_unique_tags()
                    tag = input("Podaj tag do wyszukiwania: ")
                    notebook.search_notes_by_tag(tag)
                elif note_action == 's':
                    notebook.show_unique_tags()
                    tag = input("Podaj tag po którym chcesz sortować notatki: ")
                    if notebook.sort_notes_by_tags(tag):
                        notebook.show_notes()
                    else:
                        print("Sortowanie nie zostało wykonane.")
                    if notebook.sort_notes_by_tags(tag):
                        notebook.show_notes()
                elif note_action == 'q':
                    break
                else:
                    print("Nieznana akcja, spróbuj ponownie.")
        elif action == 'q':
            print("Wyjście z programu.")
            break
        else:
            print("Nieznana akcja, spróbuj ponownie.")

    save_address_book(book)
    notebook.save_notes()

if __name__ == "__main__":
    main()
