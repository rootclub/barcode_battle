# Gestione Prezzi e Soci - ASCII Art

Questo progetto è un sistema completo per la **gestione dei prezzi** di prodotti con e senza codice a barre, e per la **gestione dei soci** (con relativo storico acquisti). Il tutto si basa su un'interfaccia testuale e sfrutta la libreria [art](https://pypi.org/project/art/) per convertire i prezzi in ASCII art, oltre alla libreria [Pillow](https://pypi.org/project/Pillow/) per la conversione delle immagini dei soci.

## Funzionalità Principali

- **Scansione Codice a Barre**: Legge il codice a barre e mostra il prezzo in ASCII art.  
  - Se il codice a barre non esiste nel database, richiede all’utente di inserire un nuovo prezzo e ne effettua il salvataggio.
- **Gestione Articoli Senza Codice a Barre**: Possibilità di memorizzare articoli che non hanno un codice a barre.
- **Gestione Soci**:
  - Registrazione nuovi soci.
  - Associazione di un’immagine del socio (convertita in ASCII art).
  - Salvataggio dello storico acquisti per ogni socio.
- **Menu di Gestione**:
  - Modifica e rimozione di prezzi e articoli.
  - Cambio del font per l’ASCII art.
  - Possibilità di abilitare/disabilitare la visualizzazione dell’immagine profilo.
- **Salvataggio CSV**: Tutti i dati (prezzi, soci, acquisti, ecc.) vengono memorizzati su file CSV per la persistenza.

## Requisiti

Per installare le dipendenze necessarie, assicurati di avere **Python 3+** installato, quindi lancia:


pip install -r requirements.txt


All’interno del file **requirements.txt** dovrai avere, come minimo:


art

Pillow


## Avvio del Programma

1. Esegui il file principale, al login:

  **1. edita il file di profilo dell'utente pi**

    nano ~/.bash_profile  

  **2. inserisci questa riga, salva ed esci.**

   /home/pi/barcode/env/bin/python /home/pi/barcode/barcode_scanner.py



2. **Menu Principale**:  
   - **1. Accesso Socio**: Modalità per caricare/acquistare prodotti da parte del socio.
   - **2. Visualizza articoli senza codice a barre**: Visualizza tutti gli articoli non associati a un barcode.
   - **3. Gestione**: Consente di modificare prezzi, prodotti, font, e togglare la visualizzazione delle immagini profilo.
   - **4. Esci**: Salvataggio dei dati e spegnimento (fittizio o reale, a seconda del sistema operativo).

3. **Scansione Codice a Barre**: In qualsiasi momento, se inserisci un codice a barre fuori dalle opzioni di menu, il programma tenterà di riconoscere il prodotto e mostrare il prezzo in ASCII art.

## Licenza

Questo progetto è liberamente modificabile e distribuibile a patto di rispettare le licenze delle librerie utilizzate (ad esempio [art](https://pypi.org/project/art/) e [Pillow](https://pypi.org/project/Pillow/)).

---

Buon divertimento!