#!/usr/bin/env python3
import csv
import os
from art import text2art
from PIL import Image
from typing import Dict, List, Tuple

# Variabile globale per controllare la visualizzazione dell'immagine del socio
SHOW_PROFILE_IMAGE = False

# ------------------------------
# Funzioni di utilità
# ------------------------------

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def image_to_ascii(image_path: str, new_width: int = 80) -> str:
    """
    Converte un'immagine in ASCII art.
    :param image_path: percorso dell'immagine.
    :param new_width: larghezza desiderata per l'output ASCII.
    :return: stringa contenente l'ASCII art o un messaggio d'errore.
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        return f"Errore nel caricamento dell'immagine: {e}"
    # Converti in scala di grigi
    image = image.convert("L")
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    image = image.resize((new_width, new_height))
    pixels = image.getdata()
    # Caratteri da più scuri a più chiari
    ascii_chars = "@%#*+=-:. "
    new_pixels = [ascii_chars[pixel * len(ascii_chars) // 256] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    ascii_image = "\n".join(new_pixels[i:i+new_width] for i in range(0, len(new_pixels), new_width))
    return ascii_image

# ------------------------------
# Gestione dei prodotti con codice a barre
# ------------------------------

def load_prices(csv_file: str) -> Dict[str, str]:
    """Carica i prezzi dal file CSV in un dizionario {barcode: price}."""
    prices: Dict[str, str] = {}
    try:
        with open(csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                prices[row["barcode"]] = row["price"]
    except FileNotFoundError:
        print(f"Il file {csv_file} non esiste. Verrà creato alla prima aggiunta di un prezzo.")
    return prices

def save_prices(csv_file: str, prices: Dict[str, str]) -> None:
    """Salva i prodotti (con codice a barre) nel file CSV."""
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["barcode", "price"])
        writer.writeheader()
        for barcode, price in prices.items():
            writer.writerow({"barcode": barcode, "price": price})

# ------------------------------
# Gestione degli articoli SENZA codice a barre
# ------------------------------

def load_no_barcode_items(csv_file: str) -> Dict[str, str]:
    """Carica gli articoli senza codice a barre dal file CSV in un dizionario {description: price}."""
    items: Dict[str, str] = {}
    try:
        with open(csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                items[row["description"]] = row["price"]
    except FileNotFoundError:
        print(f"Il file {csv_file} non esiste. Verrà creato alla prima aggiunta di un articolo.")
    return items

def save_no_barcode_items(csv_file: str, items: Dict[str, str]) -> None:
    """Salva gli articoli senza codice a barre nel file CSV."""
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["description", "price"])
        writer.writeheader()
        for description, price in items.items():
            writer.writerow({"description": description, "price": price})

# ------------------------------
# Funzioni per la visualizzazione in ASCII art (per i prezzi)
# ------------------------------

def display_ascii_art(price: str, font: str) -> None:
    """Mostra il prezzo in ASCII art usando il font specificato."""
    clear_screen()
    ascii_art = text2art(price, font=font)
    print(ascii_art)

def handle_barcode(barcode: str, prices: Dict[str, str], font: str) -> None:
    """Se il codice a barre esiste, mostra il prezzo in ASCII art; altrimenti chiede il prezzo."""
    clear_screen()
    if barcode in prices:
        display_ascii_art(prices[barcode], font)
    else:
        print("Codice a barre non trovato nel database.")
        new_price = input("Inserisci il prezzo per questo codice a barre: ").strip()
        prices[barcode] = new_price
        print("Prezzo aggiunto al database.")

def remove_code(prices: Dict[str, str]) -> None:
    """Rimuove un prodotto con codice a barre dal database."""
    barcode = input("Inserisci il codice a barre da rimuovere: ").strip()
    if barcode in prices:
        del prices[barcode]
        print("Codice a barre rimosso dal database.")
    else:
        print("Codice a barre non trovato.")

def list_barcode_items(prices: Dict[str, str]) -> None:
    """Visualizza i prodotti con codice a barre."""
    if not prices:
        print("Nessun articolo con codice a barre trovato.")
    else:
        print("Articoli con codice a barre:")
        for barcode, price in prices.items():
            print(f"{barcode} -> {price}")

# ------------------------------
# Funzioni per gli articoli SENZA codice a barre
# ------------------------------

def list_no_barcode_items(items: Dict[str, str]) -> None:
    """Visualizza gli articoli senza codice a barre."""
    if not items:
        print("Nessun articolo senza codice a barre trovato.")
    else:
        print("Articoli senza codice a barre:")
        for description, price in items.items():
            print(f"{description} -> {price}")

def add_no_barcode_item(items: Dict[str, str]) -> None:
    """Aggiunge un nuovo articolo senza codice a barre."""
    description = input("Inserisci la descrizione del prodotto: ").strip()
    if description in items:
        print("Il prodotto esiste già.")
    else:
        price = input("Inserisci il prezzo: ").strip()
        items[description] = price
        print("Prodotto aggiunto.")

def remove_no_barcode_item(items: Dict[str, str]) -> None:
    """Rimuove un articolo senza codice a barre dal database tramite indice."""
    if not items:
        print("Nessun articolo senza codice a barre da rimuovere.")
        return
    items_list = list(items.items())
    print("Articoli senza codice a barre:")
    for i, (desc, price) in enumerate(items_list, start=1):
        print(f"{i}. {desc} -> {price}")
    idx_str = input("Inserisci l'indice dell'articolo da rimuovere: ").strip()
    try:
        idx = int(idx_str)
        if 1 <= idx <= len(items_list):
            desc_to_remove = items_list[idx - 1][0]
            del items[desc_to_remove]
            print("Articolo rimosso dal database.")
        else:
            print("Indice non valido.")
    except ValueError:
        print("Input non valido, devi inserire un numero.")

def select_font() -> str:
    """Permette di selezionare il font per l'ASCII art dei prezzi."""
    fonts = [
        "type_set", "xtty", "xsansb", "roman", "poison",
        "nancyj", "katakana", "inc_raw", "future_7",
        "fp2", "fireing", "fair_mea", "ebbs_2", "clb8x10"
    ]
    print("Font disponibili:")
    for i, f in enumerate(fonts, 1):
        print(f"{i}. {f}")
    while True:
        choice = input("Seleziona un font (1-14): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(fonts):
            return fonts[int(choice)-1]
        print("Scelta non valida, riprova.")

# ------------------------------
# Gestione dei soci e degli acquisti
# ------------------------------
# I soci sono memorizzati in un file CSV con i campi:
# member_code, name, image_path

def load_members(csv_file: str) -> Dict[str, Tuple[str, str]]:
    """Carica i soci dal file CSV e restituisce un dizionario {member_code: (name, image_path)}."""
    members: Dict[str, Tuple[str, str]] = {}
    try:
        with open(csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                members[row["member_code"]] = (row["name"], row["image_path"])
    except FileNotFoundError:
        print(f"Il file {csv_file} non esiste. Verrà creato al primo salvataggio.")
    return members

def save_members(csv_file: str, members: Dict[str, Tuple[str, str]]) -> None:
    """Salva i soci nel file CSV."""
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["member_code", "name", "image_path"])
        writer.writeheader()
        for member_code, (name, image_path) in members.items():
            writer.writerow({"member_code": member_code, "name": name, "image_path": image_path})

def load_purchases(csv_file: str) -> Dict[str, List[Tuple[str, str]]]:
    """Carica gli acquisti dal file CSV e restituisce {member_code: [(product, price), ...]}."""
    purchases: Dict[str, List[Tuple[str, str]]] = {}
    try:
        with open(csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                member_code = row["member_code"]
                product = row["product"]
                price = row["price"]
                if member_code not in purchases:
                    purchases[member_code] = []
                purchases[member_code].append((product, price))
    except FileNotFoundError:
        print(f"Il file {csv_file} non esiste. Verrà creato al primo salvataggio.")
    return purchases

def save_purchases(csv_file: str, purchases: Dict[str, List[Tuple[str, str]]]) -> None:
    """Salva gli acquisti nel file CSV."""
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["member_code", "product", "price"])
        writer.writeheader()
        for member_code, items in purchases.items():
            for product, price in items:
                writer.writerow({"member_code": member_code, "product": product, "price": price})

def register_member(members: Dict[str, Tuple[str, str]]) -> None:
    """Registra un nuovo socio, includendo il percorso dell'immagine."""
    member_code = input("Inserisci il codice del socio: ").strip()
    if member_code in members:
        print("Il socio esiste già.")
    else:
        name = input("Inserisci il nome del socio: ").strip()
        image_path = input("Inserisci il percorso dell'immagine del socio (lascia vuoto per default): ").strip()
        if not image_path:
            image_path = "default_image.jpg"  # Imposta un'immagine di default
        members[member_code] = (name, image_path)
        print("Socio registrato.")

def member_mode(members: Dict[str, Tuple[str, str]],
                purchases: Dict[str, List[Tuple[str, str]]],
                prices: Dict[str, str],
                no_barcode_items: Dict[str, str],
                current_font: str) -> None:
    """
    Modalità Socio: consente al socio di:
      - Scansionare prodotti (con codice a barre) e visualizzarne il prezzo in ASCII art,
      - Aggiungere prodotti senza codice a barre scegliendoli dall'elenco,
      - Visualizzare e modificare la lista degli acquisti (con possibilità di rimuovere per indice),
      - Azzerare il conto.
    In ogni menu viene (opzionalmente) visualizzato il nome del socio e la sua immagine (convertita in ASCII art).
    """
    member_code = input("Inserisci il codice del socio: ").strip()
    if member_code not in members:
        print("Socio non trovato. Vuoi registrarlo? (s/n)")
        if input().strip().lower() == "s":
            register_member(members)
        else:
            return
    member_name, image_path = members[member_code]
    if SHOW_PROFILE_IMAGE:
        print(f"\nImmagine del socio {member_name}:")
        ascii_image = image_to_ascii(image_path, new_width=80)
        print(ascii_image)
    
    if member_code not in purchases:
        purchases[member_code] = []
    while True:
        print(f"\nModalità Socio - Socio: {member_name}")
        print("1. Scansiona prodotto (con codice a barre)")
        print("2. Aggiungi prodotto senza codice a barre (scegli dall'elenco)")
        print("3. Visualizza acquisti")
        print("4. Rimuovi prodotto dalla lista degli acquisti")
        print("5. Azzera il conto")
        print("6. Esci dalla modalità socio")
        choice = input("Seleziona un'opzione: ").strip()
        if choice == "1":
            barcode = input("Scansiona il codice a barre del prodotto: ").strip()
            if barcode in prices:
                display_ascii_art(prices[barcode], current_font)
                product_price = prices[barcode]
                purchases[member_code].append((barcode, product_price))
                print("Prodotto aggiunto alla lista degli acquisti.")
            else:
                print("Codice a barre non trovato nel database prodotti.")
                new_price = input("Inserisci il prezzo per questo prodotto: ").strip()
                prices[barcode] = new_price
                display_ascii_art(new_price, current_font)
                purchases[member_code].append((barcode, new_price))
                print("Prodotto aggiunto al database e alla lista degli acquisti.")
        elif choice == "2":
            if not no_barcode_items:
                print("Nessun prodotto senza codice a barre disponibile.")
            else:
                items_list = list(no_barcode_items.items())
                print("Prodotti senza codice a barre disponibili:")
                for i, (desc, price) in enumerate(items_list, start=1):
                    print(f"{i}. {desc} -> {price}")
                idx_str = input("Seleziona l'indice del prodotto da aggiungere: ").strip()
                try:
                    idx = int(idx_str)
                    if 1 <= idx <= len(items_list):
                        selected = items_list[idx - 1]
                        desc, price = selected
                        display_ascii_art(price, current_font)
                        purchases[member_code].append((desc, price))
                        print("Prodotto aggiunto alla lista degli acquisti.")
                    else:
                        print("Indice non valido.")
                except ValueError:
                    print("Input non valido, deve essere un numero.")
        elif choice == "3":
            if not purchases.get(member_code):
                print("Nessun acquisto registrato.")
            else:
                total = 0.0
                print(f"\nAcquisti del socio {member_name}:")
                for i, (prod, price) in enumerate(purchases[member_code], start=1):
                    print(f"{i}. {prod} -> {price}")
                    try:
                        total += float(price)
                    except ValueError:
                        pass
                print(f"Totale: {total:.2f}")
        elif choice == "4":
            if not purchases.get(member_code):
                print("La lista degli acquisti è vuota.")
            else:
                items_list = purchases[member_code]
                print("Prodotti acquistati:")
                for i, (prod, price) in enumerate(items_list, start=1):
                    print(f"{i}. {prod} -> {price}")
                idx_str = input("Inserisci l'indice del prodotto da rimuovere: ").strip()
                try:
                    idx = int(idx_str)
                    if 1 <= idx <= len(items_list):
                        removed = items_list.pop(idx - 1)
                        print(f"Prodotto '{removed[0]}' rimosso dalla lista degli acquisti.")
                    else:
                        print("Indice non valido.")
                except ValueError:
                    print("Input non valido, deve essere un numero.")
        elif choice == "5":
            purchases[member_code] = []
            print("Il conto è stato azzerato.")
        elif choice == "6":
            break
        else:
            print("Opzione non valida.")

# ------------------------------
# Menu Principale e Sottomenu Gestione
# ------------------------------

def display_gestione_menu() -> None:
    print("\nMenu Gestione:")
    print("1. Modifica un prezzo")
    print("2. Rimuovi un codice a barre")
    print("3. Aggiungi un prodotto")
    print("4. Aggiungi un articolo senza codice a barre")
    print("5. Rimuovi un articolo senza codice a barre")
    print("6. Cambia font ASCII art")
    print("7. Visualizza articoli con codice a barre")
    print("8. Torna al menu principale")
    print("9. Toggle visualizzazione immagine profilo")

def gestione_menu(prices: Dict[str, str],
                  no_barcode_items: Dict[str, str],
                  current_font: str) -> str:
    while True:
        display_gestione_menu()
        choice = input("Seleziona un'opzione: ").strip()
        if choice == "1":
            barcode = input("Inserisci il codice a barre del prodotto da modificare: ").strip()
            if barcode in prices:
                print("Prezzo attuale:")
                display_ascii_art(prices[barcode], current_font)
                new_price = input("Inserisci il nuovo prezzo: ").strip()
                prices[barcode] = new_price
                print("Prezzo aggiornato.")
            else:
                print("Codice a barre non trovato.")
        elif choice == "2":
            remove_code(prices)
        elif choice == "3":
            barcode = input("Inserisci il codice a barre: ").strip()
            if barcode in prices:
                print("Il prodotto esiste già. Usa l'opzione di modifica.")
            else:
                price = input("Inserisci il prezzo: ").strip()
                prices[barcode] = price
                print("Prodotto aggiunto.")
        elif choice == "4":
            add_no_barcode_item(no_barcode_items)
        elif choice == "5":
            remove_no_barcode_item(no_barcode_items)
        elif choice == "6":
            current_font = select_font()
            print(f"Font cambiato in: {current_font}")
        elif choice == "7":
            clear_screen()
            list_barcode_items(prices)
        elif choice == "8":
            break
        elif choice == "9":
            global SHOW_PROFILE_IMAGE
            SHOW_PROFILE_IMAGE = not SHOW_PROFILE_IMAGE
            status = "attivata" if SHOW_PROFILE_IMAGE else "disattivata"
            print(f"Visualizzazione immagine profilo {status}.")
        else:
            print("Opzione non valida.")
    return current_font

def display_main_menu() -> None:
    print("\nMenu Principale:")
    print("1. Accesso Socio")
    print("2. Visualizza articoli senza codice a barre")
    print("3. Gestione")
    print("4. Esci")

def main() -> None:
    # Nomi dei file
    database_file = "database.csv"
    no_barcode_file = "items_no_barcode.csv"
    members_file = "members.csv"
    purchases_file = "acquisti.csv"

    # Caricamento dati
    prices = load_prices(database_file)
    no_barcode_items = load_no_barcode_items(no_barcode_file)
    members = load_members(members_file)
    purchases = load_purchases(purchases_file)
    current_font = "type_set"

    while True:
        display_main_menu()
        choice = input("Seleziona un'opzione o scansiona un codice a barre: ").strip()
        if choice == "1":
            member_mode(members, purchases, prices, no_barcode_items, current_font)
        elif choice == "2":
            clear_screen()
            list_no_barcode_items(no_barcode_items)
        elif choice == "3":
            current_font = gestione_menu(prices, no_barcode_items, current_font)
        elif choice == "4":
            save_prices(database_file, prices)
            save_no_barcode_items(no_barcode_file, no_barcode_items)
            save_members(members_file, members)
            save_purchases(purchases_file, purchases)
            print("Salvataggio completato. Spegnimento in corso...")
            os.system("shutdown -h now")
            break
        else:
            handle_barcode(choice, prices, current_font)

if __name__ == "__main__":
    main()
