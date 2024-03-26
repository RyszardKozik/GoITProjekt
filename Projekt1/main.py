from address_book import AddressBook, create_record, load_address_book, \
    suggest_correction_search, suggest_closest_command, save_address_book
from notes import Notebook

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
                    print(f"Czy chodziło Ci o wybranie: {closest_command}   - dla komendy ")
        elif action == 'n':
            while True:
                note_action = input(
                    "Wybierz działanie dla notatek: \nDodaj notatkę (d), Pokaż notatki (p), "
                    "Usuń notatkę (u), Edytuj notatkę (e), Wyszukaj notatki według tagu (t), "
                    "Sortuj notatki według tagów (s), Wróć (q): ")
                if note_action == 'd':
                    title = input("Podaj tytuł notatki: ")
                    content = input("Podaj treść notatki: ")
                    tags = input(
                        "Podaj tagi oddzielone przecinkami (naciśnij Enter, aby pominąć): ").split(',')
                    tags = [tag.strip() for tag in tags if tag.strip()]
                    notebook.add_note(title, content, tags)
                    print("Dodano notatkę.")

                elif note_action == 'p':
                    notebook.show_notes()

                elif note_action == 'u':
                    note_id = int(input("Podaj ID notatki do usunięcia: "))
                    notebook.delete_note(note_id)
                    print("Usunięto notatkę.")

                elif note_action == 'e':
                    note_id = int(input("Podaj ID notatki do edycji: "))
                    title = input(
                        "Podaj nowy tytuł notatki (naciśnij Enter, aby pominąć): ")
                    content = input(
                        "Podaj nową treść notatki (naciśnij Enter, aby pominąć): ")
                    tags = input(
                        "Podaj nowe tagi oddzielone przecinkami (naciśnij Enter, aby pominąć): ").split(',')
                    notebook.edit_note(note_id, title, content, tags)
                    print("Zaktualizowano notatkę.")

                elif note_action == 't':
                    notebook.tag_manager.display_available_tags()  # Wyświetla dostępne tagi
                    input("Naciśnij Enter, aby kontynuować...")
                    tag = input("Podaj tag do wyszukiwania: ")
                    notebook.tag_manager.search_notes_by_tag(tag)

                elif note_action == 's':
                    notebook.tag_manager.display_available_tags()  # Wyświetla dostępne tagi
                    input("Naciśnij Enter, aby kontynuować...")
                    tag = input(
                        "Podaj tag po którym chcesz sortować notatki: ")
                    notebook.tag_manager.sort_notes_by_tags(tag)

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