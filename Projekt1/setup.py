from setuptools import setup, find_packages

setup(
    name='addres book',
    version='1',
    description='''Osobisty asystent powinien być w stanie: 
1. Przechowywać kontakty z nazwiskami, adresami, numerami telefonów, e-mailami i datami urodzin w książce kontaktów;
2. Wyświetlać listę kontaktów, których urodziny przypadają za określoną liczbę dni od bieżącej daty;
3. Sprawdzanie poprawności wprowadzonego numeru telefonu i adresu e-mail podczas tworzenia lub edytowania wpisu i powiadamianie użytkownika w przypadku nieprawidłowego wpisu;
4. Wyszukiwanie kontaktów wśród kontaktów w książce telefonicznej;
5. Edytowanie i usuwanie wpisów z książki kontaktów;
6. Zapisywanie notatek z informacjami tekstowymi;
7. Wyszukiwanie według notatek;
8. Edytowanie i usuwanie notatek;
9. Dodawanie tagów do notatek, słów kluczowych opisujących temat i przedmiot notatki; wyszukiwanie i sortowanie notatek według słów kluczowych (tagów); sortowanie plików w określonym folderze według kategorii
''',
    url='https://github.com/PartickPinace/GoITProjekt.git',
    author='Projekt Python grupa 3',
    author_email='komorowskimateusz96@gmail.com',
    license='MIT',
    packages=find_packages()
)