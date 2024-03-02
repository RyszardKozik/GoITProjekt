#from collections import UserDict
import re
#import pickle
#from datetime import datetime, timedelta
#from notes import Notebook
from Levenshtein import distance as levenshtein_distance

class Field:
    """Base class for entry fields."""
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

def edit_name(self, new_name: Name):
    """Changes the first and last name."""
    self.name = new_name

def suggest_correction_name(name_to_edit, matching_records):
    closest_name = min(matching_records, key=lambda x: levenshtein_distance(name_to_edit, x[0].name.value))
    return closest_name[0].name.value

def edit_record(book):
    """Edits an existing record in the address book."""
    name_to_edit = input("Wprowadź imię i nazwisko, które chcesz edytować: ")
    matching_records = book.find_records_by_name(name_to_edit)

    if not matching_records:
        print("Nie znaleziono pasujących rekordów.")
        closest_search_term = suggest_correction_name(name_to_edit, book)
        print(f"Czy chodziło Ci o: {closest_search_term}   - dla  wyszukiwania?")
        return

    if len(matching_records) > 1:
        print("Znaleziono więcej niż jeden pasujący rekord. Proszę wybrać jeden z poniższych:")
        for idx, (record_id, record) in enumerate(matching_records, start=1):
            print(f"{idx}. ID: {record_id}, Rekord: {record}")

        try:
            choice_idx = int(input("Wybierz numer rekordu do edycji: "))
            if 0 < choice_idx <= len(matching_records):
                record_id, record = matching_records[choice_idx - 1]
            else:
                print("Nieprawidłowy numer rekordu.")
                return
        except ValueError:
            print("Nieprawidłowa wartość. Wprowadź numer.")
            return
    else:
        record_id, record = matching_records[0]

    print(f"Edytowanie: ID: {record_id}, {name_to_edit}.")

    # Edycja imienia i nazwiska
    new_name_input = input("Podaj nowe imię i nazwisko (wciśnij Enter, aby zachować obecne): ")
    if new_name_input.strip():
        record.edit_name(Name(new_name_input))
        print("Zaktualizowano imię i nazwisko.")

    # Edycja numerów telefonów
    if record.phones:
        print("Obecne numery telefonów: ")
        for idx, phone in enumerate(record.phones, start=1):
            print(f"{idx}. {phone.value}")
        phone_to_edit = input("Podaj numer telefonu do edycji (wciśnij Enter, aby zachować obecny): ")
        idxx = idx - 1
        while True:
            if phone_to_edit.strip():
                if len(phone_to_edit) == 9 and phone_to_edit[0] != '0' and phone_to_edit.isdigit():
                    record.phones[idxx].value = phone_to_edit  # Zaktualizowanie numeru telefonu
                    print("Numer telefonu zaktualizowany.")
                    print(f"{idx}. {phone_to_edit}")
                    break
                else:
                    print("Nieprawidłowy numer telefonu. Numer telefonu musi mieć dokładnie 9 cyfr, nie może zaczynać się od zera.")
                    phone_to_edit = input("Podaj poprawny numer telefonu: ")

    # Edycja email
    if record.emails:
        print("Obecne adresy e-mail: ")
        for idx, email in enumerate(record.emails, start=1):
            print(f"{idx}. {email.value}")
        email_to_edit = input("Podaj adres e-mail do edycji (wciśnij Enter, aby zachować obecny): ")
        idxx = idx - 1
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        while True:
            if email_to_edit.strip():
                if re.match(pattern, email_to_edit):
                    record.emails[idxx].value = email_to_edit  # Zaktualizowanie numeru telefonu
                    print("adres email zaktualizowany.")
                    print(f"{idx}. {email_to_edit}")
                    break
                else:
                    print("Nieprawidłowa konwencja adresu email. ")
                    email_to_edit = input("Podaj poprawny email: ")
