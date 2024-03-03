import os

class Notes:

    def __init__(self):
        self.list_notes = 'list_notes.txt'  # Przeniesienie nazwy pliku do atrybutu klasy

    def create_note(self, file, note):
        file_name = f"{file}.txt"
        with open(file_name, 'w') as fh:
            fh.write(note)
        with open(self.list_notes, 'a') as f:
            f.write(f"{file}\n")  # Zapis nazwy notatki do listy notatek

    def search_notes(self, keyword):
        with open(self.list_notes, 'r') as fh:
            notes = fh.readlines()
        found = False

        for note in notes:
            note = note.strip()
            if keyword == note:
                name_notes = f"{keyword}.txt"
                print('\nNotatka o podanym tytule istnieje, a oto jej zawartość: \n')
                with open(name_notes, 'r') as fh:
                    content = fh.read()
                    print(content)
                found = True
                break  # Przerwanie pętli po znalezieniu notatki
        if not found:
            print('\nBrak notatki o podanym tytule\n')

    def edit_notes(self, keyword):
        with open(self.list_notes, 'r') as fh:
            notes = fh.readlines()
        found = False

        for note in notes:
            note = note.strip()
            if keyword == note:
                name_notes = f"{keyword}.txt"
                new_notes = input('Wprowadź nową notatkę: ')
                with open(name_notes, 'w') as fh:
                    fh.write(new_notes)
                    print('Notatka została zaktualizowana')
                    found = True
                    break  # Przerwanie pętli po edycji notatki
        if not found:
            print('Notatka o takiej nazwie nie istnieje')

    def remove_notes(self, keyword):
        name_note = f"{keyword}.txt"

        if os.path.exists(name_note):
            os.remove(name_note)
            with open(self.list_notes, 'r') as fh:
                notes = [note.strip() for note in fh.readlines()]
            if keyword in notes:
                notes.remove(keyword)
                with open(self.list_notes, 'w') as fh:
                    for note in notes:
                        fh.write(f"{note}\n")
                print(f'Notatka "{keyword}" została usunięta.')
        else:
            print('Notatka o podanej nazwie nie istnieje')

def main():
    notes = Notes()

    while True:
        action = input("Wybierz akcję: \nZarządzaj notatkami (n), albo Wyjdź (q): ")

        if action == 'n':
            while True:
                note_action = input("Wybierz działanie dla notatek: \nDodaj notatkę (d), Wyszukaj notatki (p), Edytuj notatkę (e), Usuń notatkę (u), Wróć (q): ")
                if note_action == 'd':
                    file = input('Wprowadź tytuł notatki: ')
                    note = input('Wprowadź notatkę: ')
                    notes.create_note(file, note)
                    print('Notatka utworzona pomyślnie')
                elif note_action == 'p':
                    keyword = input('Podaj tytuł notatki, którą chcesz otworzyć: ')
                    notes.search_notes(keyword)
                elif note_action == 'e':
                    keyword = input('Podaj nazwę notatki, którą chcesz edytować: ')
                    notes.edit_notes(keyword)
                elif note_action == 'u':
                    keyword = input('Wprowadź nazwę notatki, którą chcesz usunąć: ')
                    notes.remove_notes(keyword)
                elif note_action == 'q':
                    break
                else:
                    print("Nieznana akcja, spróbuj ponownie.")
        elif action == 'q':
            print("Wyjście z programu.")
            break
        else:
            print("Nieznana akcja, spróbuj ponownie.")

if __name__ == "__main__":
    main()
