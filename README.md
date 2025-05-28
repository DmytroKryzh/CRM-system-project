# CRM-system-project
Opis

CRM FINANSE to konsolowa aplikacja, przeznaczona do zarządzania klientami oraz produktami finansowymi w małej instytucji finansowej. Program umożliwia przechowywanie i edycję danych klientów, zarządzanie ofertą produktów finansowych, przypisywanie produktów do klientów, generowanie raportów oraz eksport danych do pliku CSV. Wszystkie dane są zapisywane w lokalnej bazie danych SQLite.

Funkcje programu

Dodawanie klienta — wprowadź dane osobowe, PESEL, kontakt, datę urodzenia.
Edycja klienta — zmień dane wybranego klienta.
Usuwanie klienta — usuń klienta oraz powiązane z nim produkty.
Wyświetlanie wszystkich klientów — przejrzysta lista wszystkich klientów w bazie.
Dodawanie produktu finansowego — wprowadź nazwę, typ (np. kredyt, lokata), opis.
Przypisywanie produktu klientowi — wybierz klienta i produkt, określ datę oraz kwotę.
Wyświetlanie produktów klienta — sprawdź, jakie produkty posiada dany klient.
Wyszukiwanie klientów — po imieniu, nazwisku lub numerze PESEL.
Generowanie raportów/statystyk — liczba klientów, liczba produktów, suma kwot, liczba przypisań.
Eksport danych do CSV — zapis wszystkich klientów do pliku klienci.csv.

Użyte biblioteki

sqlite3 — do obsługi bazy danych SQLite.
pandas — do eksportu danych do pliku CSV.

Struktura plików

crm_finanse.py — główny plik programu (cały kod aplikacji)
crm_finanse.db — plik bazy danych SQLite (tworzony automatycznie przy pierwszym uruchomieniu)
klienci.csv — plik z wyeksportowanymi danymi klientów (tworzony po eksporcie)

Przykłady

1. Dodawanie klienta:

Imię: Jan
Nazwisko: Kowalski
PESEL: 70010112345
Email: jan.kowalski@email.com
Telefon: 123456789
Data urodzenia: 1970-01-01
2. Dodawanie klienta:

Imię: Anna
Nazwisko: Nowak
PESEL: 80020254321
Email: anna.nowak@email.com
Telefon: 987654321
Data urodzenia: 1980-02-02
3. Dodawanie produktu finansowego:

Nazwa: Kredyt hipoteczny
Typ: kredyt
Opis: Kredyt na zakup mieszkania
4. Dodawanie produktu finansowego:

Nazwa: Lokata terminowa
Typ: lokata
Opis: Lokata na 12 miesięcy
5. Przypisywanie produktu klientowi:

ID klienta: 1 (Jan Kowalski)
ID produktu: 3 (Kredyt hipoteczny)
Data przydzielenia: 2024-05-28
Kwota: 200000
6. Przypisywanie produktu klientowi:

ID klienta: 2 (Anna Nowak)
ID produktu: 4 (Lokata terminowa)
Data przydzielenia: 2024-05-28
Kwota: 10000
7. Edycja klienta:

ID klienta: 1 (Jan Kowalski)
Nowy email: j.kowalski@nowyemail.com
8. Wyszukiwanie klienta:

Kryterium: Nazwisko
Wartość: Nowak
Oczekiwany wynik: Anna Nowak
9. Generowanie raportu:

Oczekiwany wynik:
Liczba klientów: 2
Liczba produktów: 2
Liczba przypisań: 2
Suma kwot: 210000
10. Eksport do CSV:

Oczekiwany wynik: Plik klienci.csv zawierający dane Jana Kowalskiego i Anny Nowak.


