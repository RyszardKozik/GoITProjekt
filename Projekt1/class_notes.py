import os


class Notes():

    def create_note(self, file, note):
        file_name = str(file + '.txt').strip()
        with open(file_name, 'w') as fh:
            fh.write(note)
        name_notes = ''
        name_notes += (file + '\n')
        with open(list_notes, 'a') as f:
            f.write(str(name_notes))

    def search_notes(self, keyword):
        result_list = []
        with open('list_notes.txt', 'r') as fh:
            notes = fh.readlines()
            found = False

            for note in notes:
                note = note.replace('\n', '')
                result_list.append(note)

                if keyword == note:
                    name_notes = str(keyword + '.txt')
                    print()
                    print('Notatka o podanym tytule istnieje, a oto jej zawartość: \n')
                    with open(name_notes, 'r') as fh:
                        content = fh.read()
                        print(content)
                    found = True
            if not found:
                print()
                print('Brak notatki o podanym tytule')

        print()

    def edit_notes(self, keyword):
        result_list = []
        with open('list_notes.txt', 'r') as fh:
            notes = fh.readlines()
            found = False

            for note in notes:
                note = note.replace('\n', '')
                result_list.append(note)
                if keyword == note:
                    name_notes = str(keyword + '.txt')
                    new_notes = input('Wprowadź nową notatkę: ')
                    with open(name_notes, '+w') as fh:
                        fh.write(new_notes)
                        print('Notatka została zaktualizowana')
                        found = True
            if not found:
                print('Notatka o takiej nazwie nie istnieje')

    def remove_notes(self, keyword):
        name_note = str(keyword + '.txt')
        result_list = []

        if os.path.exists(name_note):
            os.remove(name_note)

            with open('list_notes.txt', 'r') as fh:
                notes = fh.readlines()
                for note in notes:
                    note = note.replace('\n', '')
                    result_list.append(note)

                if keyword == note:
                    note_index = result_list.index(keyword)
                    if 0 < note_index < len(notes):
                        remove_note = notes.pop(note_index)
                        with open('list_notes.txt', 'w') as fh:
                            fh.writelines(notes)
                        print(f'Notatka została usunięta: {
                            remove_note.strip()}')
        else:
            print('Notatka o podanej nazwie nie istnieje')


def main():
    notes = Notes()

    while True:
        action = input(
            "Wybierz akcję: \nZarządzaj Kontaktami (z), Zarządzaj notatkami (n), albo Wyjdź (q): ")

        if action == 'n':
            while True:
                note_action = input(
                    "Wybierz działanie dla notatek: \nDodaj notatkę (d), Wyszukaj notatki (p), Edytuj notatke (e)"
                    "Usuń notatkę (u), Wróć (q): ")
                if note_action == 'd':
                    file = input('Wprowadź tytul notatki: ')
                    note = input('Wprowadź notatkę: ')
                    notes.create_note(file, note)
                    print('Notatka utworzona pomyślnie')

                elif note_action == 'p':
                    keyword = (
                        input('Podaj tytul notatki, którą chcesz otworzyc: '))
                    notes.search_notes(keyword)

                elif note_action == 'e':
                    keyword = input(
                        'Podaj nazwę notatki którą chcesz edytować: ')
                    notes.edit_notes(keyword)

                elif note_action == 'u':
                    keyword = input(
                        'Wprowadz nazwe notatki, którą chcesz usunąć: ')
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


list_notes = 'list_notes.txt'

if __name__ == "__main__":
    main()
