# Importujemy potrzebne biblioteki
import sqlite3  # Do obsługi bazy danych SQLite
import pandas as pd  # Do eksportu danych do pliku CSV
import datetime  # Do obsługi dat
import sys  # Do obsługi wyjścia z programu

# ----------------------------------------------
# Blok: Inicjalizacja bazy danych i połączenia
# ----------------------------------------------

def inicjalizuj_baze():
    conn = sqlite3.connect('crm_finanse.db')
    c = conn.cursor()
    # Tworzymy tabelę klientów
    c.execute('''
        CREATE TABLE IF NOT EXISTS klienci (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL,
            pesel TEXT UNIQUE NOT NULL,
            email TEXT,
            telefon TEXT,
            data_urodzenia TEXT
        )
    ''')
    # Tworzymy tabelę produktów finansowych
    c.execute('''
        CREATE TABLE IF NOT EXISTS produkty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL,
            typ TEXT NOT NULL,
            opis TEXT
        )
    ''')
    # Tworzymy tabelę powiązań klient-produkt
    c.execute('''
        CREATE TABLE IF NOT EXISTS klient_produkty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            klient_id INTEGER,
            produkt_id INTEGER,
            data_przydzielenia TEXT,
            kwota REAL,
            FOREIGN KEY(klient_id) REFERENCES klienci(id),
            FOREIGN KEY(produkt_id) REFERENCES produkty(id)
        )
    ''')
    conn.commit()
    return conn

# ----------------------------------------------
# Blok: Funkcje pomocnicze do obsługi menu
# ----------------------------------------------

def wyswietl_menu():
    print("\n=== CRM FINANSE - MENU GŁÓWNE ===")
    print("1. Dodaj klienta")
    print("2. Edytuj klienta")
    print("3. Usuń klienta")
    print("4. Wyświetl wszystkich klientów")
    print("5. Dodaj produkt finansowy")
    print("6. Przypisz produkt klientowi")
    print("7. Wyświetl produkty klienta")
    print("8. Wyszukaj klienta")
    print("9. Generuj raport/statystyki")
    print("10. Eksportuj dane do CSV")
    print("0. Wyjście")

def pobierz_wybor():
    try:
        wybor = int(input("Wybierz opcję: "))
        return wybor
    except ValueError:
        print("Błąd: Wprowadź liczbę!")
        return -1

# ----------------------------------------------
# Blok: Operacje na klientach
# ----------------------------------------------

def dodaj_klienta(conn):
    print("\n--- Dodawanie nowego klienta ---")
    imie = input("Imię: ")
    nazwisko = input("Nazwisko: ")
    pesel = input("PESEL: ")
    email = input("Email: ")
    telefon = input("Telefon: ")
    data_urodzenia = input("Data urodzenia (YYYY-MM-DD): ")
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO klienci (imie, nazwisko, pesel, email, telefon, data_urodzenia)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (imie, nazwisko, pesel, email, telefon, data_urodzenia))
        conn.commit()
        print("Klient został dodany.")
    except sqlite3.IntegrityError:
        print("Błąd: Klient o podanym PESEL już istnieje.")

def edytuj_klienta(conn):
    print("\n--- Edycja klienta ---")
    id_klienta = input("Podaj ID klienta do edycji: ")
    c = conn.cursor()
    c.execute("SELECT * FROM klienci WHERE id=?", (id_klienta,))
    klient = c.fetchone()
    if klient:
        print(f"Obecne dane: Imię: {klient[1]}, Nazwisko: {klient[2]}, PESEL: {klient[3]}")
        imie = input("Nowe imię (pozostaw puste, aby nie zmieniać): ") or klient[1]
        nazwisko = input("Nowe nazwisko: ") or klient[2]
        email = input("Nowy email: ") or klient[4]
        telefon = input("Nowy telefon: ") or klient[5]
        data_urodzenia = input("Nowa data urodzenia (YYYY-MM-DD): ") or klient[6]
        c.execute('''
            UPDATE klienci SET imie=?, nazwisko=?, email=?, telefon=?, data_urodzenia=?
            WHERE id=?
        ''', (imie, nazwisko, email, telefon, data_urodzenia, id_klienta))
        conn.commit()
        print("Dane klienta zostały zaktualizowane.")
    else:
        print("Nie znaleziono klienta o podanym ID.")

def usun_klienta(conn):
    print("\n--- Usuwanie klienta ---")
    id_klienta = input("Podaj ID klienta do usunięcia: ")
    c = conn.cursor()
    c.execute("SELECT * FROM klienci WHERE id=?", (id_klienta,))
    klient = c.fetchone()
    if klient:
        c.execute("DELETE FROM klient_produkty WHERE klient_id=?", (id_klienta,))
        c.execute("DELETE FROM klienci WHERE id=?", (id_klienta,))
        conn.commit()
        print("Klient został usunięty.")
    else:
        print("Nie znaleziono klienta o podanym ID.")

def wyswietl_klientow(conn):
    print("\n--- Lista wszystkich klientów ---")
    c = conn.cursor()
    c.execute("SELECT * FROM klienci")
    klienci = c.fetchall()
    if klienci:
        print("{:<5} {:<15} {:<15} {:<12} {:<20} {:<12} {:<12}".format(
            "ID", "Imię", "Nazwisko", "PESEL", "Email", "Telefon", "Data ur."))
        for k in klienci:
            print("{:<5} {:<15} {:<15} {:<12} {:<20} {:<12} {:<12}".format(
                k[0], k[1], k[2], k[3], k[4], k[5], k[6]))
    else:
        print("Brak klientów w bazie.")

# ----------------------------------------------
# Blok: Operacje na produktach finansowych
# ----------------------------------------------

def dodaj_produkt(conn):
    print("\n--- Dodawanie produktu finansowego ---")
    nazwa = input("Nazwa produktu: ")
    typ = input("Typ produktu (np. kredyt, lokata): ")
    opis = input("Opis produktu: ")
    c = conn.cursor()
    c.execute('''
        INSERT INTO produkty (nazwa, typ, opis)
        VALUES (?, ?, ?)
    ''', (nazwa, typ, opis))
    conn.commit()
    print("Produkt został dodany.")

def przypisz_produkt(conn):
    print("\n--- Przypisywanie produktu klientowi ---")
    id_klienta = input("Podaj ID klienta: ")
    id_produktu = input("Podaj ID produktu: ")
    data_przydzielenia = input("Data przydzielenia (YYYY-MM-DD): ")
    kwota = input("Kwota (jeśli dotyczy): ")
    c = conn.cursor()
    c.execute("SELECT * FROM klienci WHERE id=?", (id_klienta,))
    if not c.fetchone():
        print("Nie znaleziono klienta o podanym ID.")
        return
    c.execute("SELECT * FROM produkty WHERE id=?", (id_produktu,))
    if not c.fetchone():
        print("Nie znaleziono produktu o podanym ID.")
        return
    c.execute('''
        INSERT INTO klient_produkty (klient_id, produkt_id, data_przydzielenia, kwota)
        VALUES (?, ?, ?, ?)
    ''', (id_klienta, id_produktu, data_przydzielenia, kwota))
    conn.commit()
    print("Produkt został przypisany klientowi.")

def wyswietl_produkty_klienta(conn):
    print("\n--- Produkty klienta ---")
    id_klienta = input("Podaj ID klienta: ")
    c = conn.cursor()
    c.execute('''
        SELECT p.nazwa, p.typ, kp.data_przydzielenia, kp.kwota
        FROM klient_produkty kp
        JOIN produkty p ON kp.produkt_id = p.id
        WHERE kp.klient_id=?
    ''', (id_klienta,))
    produkty = c.fetchall()
    if produkty:
        print("{:<20} {:<15} {:<15} {:<10}".format("Nazwa", "Typ", "Data", "Kwota"))
        for p in produkty:
            print("{:<20} {:<15} {:<15} {:<10}".format(p[0], p[1], p[2], str(p[3])))
    else:
        print("Klient nie ma przypisanych produktów.")

# ----------------------------------------------
# Blok: Wyszukiwanie klientów
# ----------------------------------------------

def wyszukaj_klienta(conn):
    print("\n--- Wyszukiwanie klienta ---")
    print("1. Po imieniu")
    print("2. Po nazwisku")
    print("3. Po PESEL")
    wybor = input("Wybierz kryterium: ")
    c = conn.cursor()
    if wybor == "1":
        imie = input("Podaj imię: ")
        c.execute("SELECT * FROM klienci WHERE imie LIKE ?", ('%' + imie + '%',))
    elif wybor == "2":
        nazwisko = input("Podaj nazwisko: ")
        c.execute("SELECT * FROM klienci WHERE nazwisko LIKE ?", ('%' + nazwisko + '%',))
    elif wybor == "3":
        pesel = input("Podaj PESEL: ")
        c.execute("SELECT * FROM klienci WHERE pesel=?", (pesel,))
    else:
        print("Nieprawidłowy wybór.")
        return
    wyniki = c.fetchall()
    if wyniki:
        print("{:<5} {:<15} {:<15} {:<12} {:<20} {:<12} {:<12}".format(
            "ID", "Imię", "Nazwisko", "PESEL", "Email", "Telefon", "Data ur."))
        for k in wyniki:
            print("{:<5} {:<15} {:<15} {:<12} {:<20} {:<12} {:<12}".format(
                k[0], k[1], k[2], k[3], k[4], k[5], k[6]))
    else:
        print("Brak wyników.")

# ----------------------------------------------
# Blok: Raporty i statystyki
# ----------------------------------------------

def generuj_raport(conn):
    print("\n--- Raport/statystyki ---")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM klienci")
    liczba_klientow = c.fetchone()[0]
    print(f"Liczba klientów: {liczba_klientow}")
    c.execute("SELECT COUNT(*) FROM produkty")
    liczba_produktow = c.fetchone()[0]
    print(f"Liczba produktów finansowych: {liczba_produktow}")
    c.execute("SELECT COUNT(*) FROM klient_produkty")
    liczba_przypisan = c.fetchone()[0]
    print(f"Liczba przypisań produktów do klientów: {liczba_przypisan}")
    c.execute("SELECT SUM(kwota) FROM klient_produkty")
    suma_kwot = c.fetchone()[0]
    print(f"Suma wszystkich kwot produktów: {suma_kwot if suma_kwot else 0}")

# ----------------------------------------------
# Blok: Eksport danych do pliku CSV
# ----------------------------------------------

def eksportuj_dane(conn):
    print("\n--- Eksport danych ---")
    print("Eksportuj klientów do CSV")
    c = conn.cursor()
    c.execute("SELECT * FROM klienci")
    klienci = c.fetchall()
    kolumny = [desc[0] for desc in c.description]
    df = pd.DataFrame(klienci, columns=kolumny)
    df.to_csv("klienci.csv", index=False)
    print("Dane klientów wyeksportowane do klienci.csv")

# ----------------------------------------------
# Blok: Główna pętla programu
# ----------------------------------------------

def main():
    conn = inicjalizuj_baze()
    while True:
        wyswietl_menu()
        wybor = pobierz_wybor()
        if wybor == 1:
            dodaj_klienta(conn)
        elif wybor == 2:
            edytuj_klienta(conn)
        elif wybor == 3:
            usun_klienta(conn)
        elif wybor == 4:
            wyswietl_klientow(conn)
        elif wybor == 5:
            dodaj_produkt(conn)
        elif wybor == 6:
            przypisz_produkt(conn)
        elif wybor == 7:
            wyswietl_produkty_klienta(conn)
        elif wybor == 8:
            wyszukaj_klienta(conn)
        elif wybor == 9:
            generuj_raport(conn)
        elif wybor == 10:
            eksportuj_dane(conn)
        elif wybor == 0:
            print("Zamykanie programu...")
            conn.close()
            sys.exit()
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

# ----------------------------------------------
# Blok: Uruchomienie programu
# ----------------------------------------------

if __name__ == "__main__":
    main()




