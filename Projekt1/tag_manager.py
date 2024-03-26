class TagManager:
    def __init__(self, notes):
        self.set_notes(notes)

    def set_notes(self, notes):
        self.notes = notes

    def display_available_tags(self):
        """Wyświetla dostępne tagi."""
        tags = set()
        for note in self.notes:
            tags.update(note['tags'])
        if tags:
            print("Dostępne tagi:", ', '.join(tags))
        else:
            print("Brak dostępnych tagów.")

    def search_notes_by_tag(self, tag):
        self.display_available_tags()  # Shows available tags before searching
        found_notes = [note for note in self.notes if tag in note.get('tags', [])]
        if not found_notes:
            print("Nie znaleziono notatek z podanym tagiem.")
            return
        for note in found_notes:
            print(f"Tytuł: {note['title']}\nTreść: {note['content']}\nTagi: {', '.join(note['tags'])}")

    def sort_notes_by_tags(self, tag):
        self.display_available_tags()  # Shows available tags before sorting
        tag_exists = any(tag in note.get('tags', []) for note in self.notes)
        if not tag_exists:
            print("Nie ma takiego tagu.")
            return False
        self.notes.sort(key=lambda note: list(note['tags']).count(tag), reverse=True)
        print("Posortowano notatki według tagu:", tag)
        return True