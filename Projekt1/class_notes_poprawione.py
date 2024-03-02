import os


class Notes:

    def create_note(self, file, note):
        file_name = str(file + '.txt').strip()
        with open(file_name, 'w') as fh:
            fh.write(note)
        name_notes = ''
        name_notes += (file + '\n')
        with open(list_notes, 'a') as f:
            f.write(str(name_notes))

    def search_notes(self, file):
        result_list = []
        with open(list_notes, 'r') as fh:
            notes = fh.readlines()
            found = False

            for note in notes:
                note = note.replace('\n', '')
                result_list.append(note)

                if file.lower() == note.lower():
                    name_notes = str(file + '.txt')
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

    def edit_notes(self, note_index):

        with open(list_notes, 'r') as fh:
            content = fh.readlines()
            found = False

            if 0 < note_index <= len(content):

                new_notes = input('Wprowadź nową notatkę: ')
                name_notes = (content[note_index - 1]
                              ).replace('\n', '') + '.txt'
                with open(name_notes, '+w') as fh:
                    fh.write(new_notes)
                    print('Notatka została zaktualizowana')
                    found = True
            if not found:
                print('Notatka o podanym numerze nie istnieje')

    def delete_note(self, note_index):
        with open(list_notes, 'r') as fh:
            content = fh.readlines()

            if 0 < note_index <= len(content):
                remove_note = content.pop(note_index - 1)
                with open(list_notes, 'w') as fh:
                    fh.writelines(content)
                    print(f'Notatka została usunięta: {
                        remove_note.strip()}')

                    name_note = str(remove_note.strip() + '.txt')
                    if os.path.exists(name_note):
                        os.remove(name_note)
            else:
                print('Notatka o podanym numerze nie istnieje')

    def elements_notes(self, file):
        with open(file, 'r') as fh:
            content = fh.readlines()

            for number, item in enumerate(content, start=1):
                print(f'{number}: {item}')


def main():
    notes = Notes()

    while True:
        action = input(
            "Wybierz akcję: \nZarządzaj Kontaktami (z), Zarządzaj notatkami (n), albo Wyjdź (q): ")

        if action == 'n':
            while True:
                note_action = input(
                    "Wybierz działanie dla notatek: \nDodaj notatkę (d), Lista notatek (l), Wyszukaj notatki po tytule (s), Edytuj notatke (e) "
                    "Usuń notatkę (u), Wróć (q): ")
                if note_action == 'd':
                    file = input('Wprowadź tytul notatki: ')
                    note = input('Wprowadź notatkę: ')
                    notes.create_note(file, note)
                    print('Notatka utworzona pomyślnie')

                elif note_action == 'l':
                    file = 'list_notes.txt'
                    notes.elements_notes(file)

                elif note_action == 's':
                    file = (
                        input('Podaj tytuł notatki, którą chcesz otworzyc: '))
                    notes.search_notes(file)

                elif note_action == 'e':
                    note_index = int(input(
                        'Podaj numer notatki którą chcesz edytować: '))
                    notes.edit_notes(note_index)

                elif note_action == 'u':
                    note_index = int(input(
                        'Wprowadz numer notatki, którą chcesz usunąć: '))
                    notes.delete_note(note_index)

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
