# Add these classes to your existing code

class Tag:
    """Class representing a tag for categorizing notes."""
    def __init__(self, name):
        self.name = name

class Note:
    """Class representing a note with content and tags."""
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.tags = []

    def add_tag(self, tag):
        """Adds a tag to the note."""
        self.tags.append(tag)

    def remove_tag(self, tag):
        """Removes a tag from the note."""
        self.tags.remove(tag)

class Notebook:
        # Existing code for Notebook class

    def create_note(self):
        """Creates a note with user input, including tags."""
        title = input("Enter the note title: ")
        content = input("Enter the note content: ")
        note = Note(title, content)

        # Adding tags
        while True:
            tag_input = input("Enter a tag (or press Enter to finish adding tags): ").strip()
            if not tag_input:
                break
            tag = Tag(tag_input)
            note.add_tag(tag)

        self.notes.append(note)
        print("Note created.")

    def show_notes_with_tags(self):
        """Displays all notes with their tags."""
        if not self.notes:
            print("No notes available.")
        else:
            for idx, note in enumerate(self.notes, start=1):
                print(f"{idx}. Title: {note.title}\n   Content: {note.content}")
                if note.tags:
                    print("   Tags:", ', '.join(tag.name for tag in note.tags))
                print()

    # Additional functions for managing tags

    def create_tag(self):
        """Creates a new tag."""
        tag_name = input("Enter the tag name: ")
        tag = Tag(tag_name)
        self.tags.append(tag)
        print("Tag created.")

    def show_tags(self):
        """Displays all tags."""
        if not self.tags:
            print("No tags available.")
        else:
            print("Tags:", ', '.join(tag.name for tag in self.tags))

# Update the main function to incorporate tag-related actions

def main():
    notebook = Notebook()
    notebook.load_notes()
    book = load_address_book()

    while True:
        action = input("Choose action:\nContacts (c), Notes (n), or Quit (q): ").lower()
        if action == 'c':
            while True:
                contact_action = input(
                    "Choose action: Add contact (a), Find contact (f), "
                    "Delete contact (d), Edit contact (e), Show all (s), or Back (b): ").lower()
                if contact_action == 'a':
                    record = create_record()
                    book.add_record(record)
                    print("Contact added.")
                elif contact_action == 'f':
                    search_term = input("Enter search term: ")
                    found = book.find_record(search_term)
                    for record in found:
                        print(record)
                elif contact_action == 'd':
                    book.delete_record_by_id()
                    print("Contact deleted.")
                elif contact_action == 'e':
                    print("Contact updated.")
                elif contact_action == 's':
                    book.show_all_records()
                elif contact_action == 'b':
                    break
                else:
                    print("Unknown action, try again.")
        elif action == 'n':
            while True:
                note_action = input(
                    "Choose action: Add note (a), Show notes (s), "
                    "Add tag (t), Show tags (st), or Back (b): ").lower()
                if note_action == 'a':
                    notebook.create_note()
                elif note_action == 's':
                    notebook.show_notes_with_tags()
                elif note_action == 't':
                    notebook.create_tag()
                elif note_action == 'st':
                    notebook.show_tags()
                elif note_action == 'b':
                    break
                else:
                    print("Unknown action, try again.")
        elif action == 'q':
            print("Exiting the program.")
            break
        else:
            print("Unknown action, try again.")

    save_address_book(book)
    notebook.save_notes()

if __name__ == "__main__":
    main()