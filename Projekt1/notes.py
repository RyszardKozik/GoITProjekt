import pickle
from datetime import datetime

class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        self.created_at = datetime.now()

    def __str__(self):
        return f"{self.created_at}: {self.title} - {self.content} - Tagi: {', '.join(self.tags)}"

class Notebook:
    def __init__(self):
        self.notes = [] # Lista do przechowywania notatek

    def add_note(self, title, content, tags=None):
        note = {"title": title, "content": content, "tags": tags if tags else []}
        self.notes.append(note)

    def show_notes(self):
        if not self.notes:
            print("Brak notatek do wyświetlenia.")
            return
        for note in self.notes:
            print(f"Tytuł: {note.get('title', 'Brak tytułu')}\nTreść: {note.get('content', 'Brak treści')}\nTagi: {', '.join(note.get('tags', []))}")

    def delete_note(self, note_id):
        try:
            note_id = int(note_id) # Konwersja na int
            if 0 <= note_id < len(self.notes):
                deleted_note = self.notes.pop(note_id) # Usuwa notatkę i zwraca ją
                print(f"Usunięto notatkę: {deleted_note.get('title', 'Brak tytułu')}")
            else:
                print("Notatka o podanym ID nie istnieje.")
        except ValueError:
            print("Podane ID nie jest liczbą całkowitą.")
        except IndexError:
            print("Podane ID jest poza zakresem listy notatek.")

    def edit_note(self, note_id, title=None, content=None, tags=None):
        """Edytuje notatkę o podanym ID."""
        # Konwertuj note_id na int, aby uniknąć błędu porównania typów
        note_id = int(note_id)

        if 0 <= note_id < len(self.notes):
            note = self.notes[note_id]
            if title is not None:
                note['title'] = title
            if content is not None:
                note['content'] = content
            if tags is not None:
                note['tags'] = tags
            print("Notatka zaktualizowana.")
        else:
            print("Nie znaleziono notatki o podanym ID.")

    def search_notes_by_tag(self, tag):
        # Przekształcanie tagów dla każdej notatki na sety, aby umożliwić efektywne sprawdzanie
        for note in self.notes:
            note['tags'] = set(note['tags'])
        
        # Teraz wyszukujemy notatki, które zawierają tag w zestawie tagów
        found_notes = [note for note in self.notes if tag in note['tags']]
        
        if not found_notes:
            print("Nie znaleziono notatek z podanym tagiem.")
            return
        
        for note in found_notes:
            print()
            print("Oto twoja notatka:")
            print()
            print(f"Tytuł: {note['title']}\nTreść: {note['content']}\nTagi: {', '.join(note['tags'])}")

    def save_notes(self, filename='notes.pkl'):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.notes, file)
            print("Notatki zostały zapisane.")
        except Exception as e:
            print(f"Błąd przy zapisie notatek: {e}")

    def load_notes(self, filename='notes.pkl'):
        try:
            with open(filename, 'rb') as file:
                self.notes = pickle.load(file)
            print("Notatki zostały wczytane.")
        except FileNotFoundError:
            print("Plik z notatkami nie istnieje. Tworzenie nowego pliku.")
            self.notes = []
        except Exception as e:
            print(f"Błąd przy wczytywaniu notatek: {e}")

    
    def sort_notes_by_tags(self, tag):
        """Sortuje notatki według liczby wystąpień wprowadzonego tagu."""
        # Sprawdzenie czy tag istnieje w notatkach
        tag_exists = any(tag in note['tags'] for note in self.notes)
        if not tag_exists:
            return False # Tag nie istnieje, zwróć False

        # sortowanie notatki według liczby wystąpień tagu
        self.notes.sort(key=lambda note: list(note['tags']).count(tag), reverse=True)
        return True
