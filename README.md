# CRM-system-project
Opis

CRM FINANSE to konsolowa aplikacja napisana w języku Python, przeznaczona do zarządzania klientami oraz produktami finansowymi w małej instytucji finansowej. Program umożliwia przechowywanie i edycję danych klientów, zarządzanie ofertą produktów finansowych, przypisywanie produktów do klientów, generowanie raportów oraz eksport danych do pliku CSV. Wszystkie dane są zapisywane w lokalnej bazie danych SQLite.

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

Struktura plików

crm_finanse.py — główny plik programu (cały kod aplikacji)
crm_finanse.db — plik bazy danych SQLite (tworzony automatycznie przy pierwszym uruchomieniu)
klienci.csv — plik z wyeksportowanymi danymi klientów (tworzony po eksporcie)


