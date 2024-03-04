# GoITProjekt

Osobisty asystent do zarządzania kontaktami i notatkami.

## Instalacja

1. **Klonowanie repozytorium**:
    - Klonowanie repozytorium: Sklonuj repozytorium projektu na swoje lokalne środowisko. Możesz to zrobić za pomocą git, używając poniższego polecenia w terminalu:
    "git clone https://github.com/PartickPinace/GoITProjekt.git"

2. **Instalacja zalezności**: 
    - Instalacja zależności: Przejdź do katalogu projektu i zainstaluj wymagane zależności. W projekcie użyto biblioteki python-Levenshtein do obliczania odległości Levenshteina, 
    która jest używana do sugestowania poprawek w przypadku błędów wprowadzania danych. Możesz zainstalować tę bibliotekę za pomocą pip:
    "cd GoITProjekt
    pip install python-Levenshtein"

3. **Uruchomienie programu**: 
    - Program można uruchomić za pomocą pliku main.py. W terminalu, w katalogu głównym projektu, wpisz: 
    "python main.py"

4. **Uzytkowanie programu**:

    Po uruchomieniu programu, zostaniesz zapytany o wybór akcji. Program oferuje dwie główne kategorie: zarządzanie kontaktami (z) i zarządzanie notatkami (n).

    - Zarządzanie kontaktami
        1. Dodawanie kontaktu: Wybierz d, aby dodać nowy kontakt. Program poprosi o wprowadzenie danych kontaktu.
        2. Znajdowanie kontaktu: Wybierz z, aby wyszukać kontakt. Program poprosi o wprowadzenie frazy wyszukiwania.
        3. Usuwanie kontaktu: Wybierz u, aby usunąć kontakt. Program poprosi o wprowadzenie ID kontaktu do usunięcia.
        4. Edycja kontaktu: Wybierz e, aby edytować istniejący kontakt. Program poprosi o wprowadzenie imienia i nazwiska kontaktu do edycji, a następnie o nowe dane.
        5. Pokazywanie wszystkich kontaktów: Wybierz p, aby zobaczyć listę wszystkich kontaktów.
    - Zarządzanie notatkami
        1. Dodawanie notatki: Wybierz d, aby dodać nową notatkę. Program poprosi o wprowadzenie tytułu, treści i tagów notatki.
        2. Pokazywanie notatek: Wybierz p, aby zobaczyć listę wszystkich notatek.
        3. Usuwanie notatki: Wybierz u, aby usunąć notatkę. Program poprosi o wprowadzenie ID notatki do usunięcia.
        4. Edycja notatki: Wybierz e, aby edytować istniejącą notatkę. Program poprosi o wprowadzenie ID notatki, a następnie o nowy tytuł, treść i tagi.
        5. Wyszukiwanie notatek według tagu: Wybierz t, aby wyszukać notatki według tagu. Program poprosi o wprowadzenie tagu do wyszukiwania.
        6. Sortowanie notatek według tagów: Wybierz s, aby posortować notatki według tagów. Program poprosi o wprowadzenie tagu, według którego chcesz posortować notatki.

5. **Zakończenie**:
    - Aby zakończyć działanie programu, wybierz q w głównym menu. Program zapyta, czy chcesz wyjść z programu, a następnie zakończy działanie.



