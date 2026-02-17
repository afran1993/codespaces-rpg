Ogni volta che implementeremo una nuova classe, faremo riferimento a questo schema per assicurarci che i 1600 elementi siano coerenti tra loro.
ARCHITETTURA DEL PROGETTO: VERTICAL REALM RPG (COMPLEX)
1. STRUTTURA CARTELLE (FOLDER TREE)

VerticalRealm_RPG/
├── main.py (Entry point & Game Loop)
├── core/
│   ├── engine.py (Gestore turni e logica verticale)
│   └── dice.py (Sistema D20 per probabilità ed eventi)
├── entities/
│   ├── base_entity.py (Classe madre per statistiche comuni)
│   ├── enemies.py (Gestore dei 1600 nemici - Data Driven)
│   └── npcs.py (Gestore dei 1600 NPC - Data Driven)
├── world/
│   ├── map_system.py (Gestore 1600 luoghi e 16 direzioni)
│   └── events.py (Classe per la gestione eventi casuali/scriptati)
├── items/
│   ├── inventory.py (Gestione zaino e pesi)
│   ├── gear.py (Classe per le 320 armi)
│   └── consumables.py (Classe per i 1600 item: pozioni, chiavi, mana)
└── data/ (Database JSON per il caricamento dinamico)
├── enemies_db.json
├── items_db.json
├── map_db.json
└── events_db.json
2. PILASTRI TECNICI DI IMPLEMENTAZIONE

    SCALABILITÀ (1600+): Nessun elemento è cablato nel codice (hardcoded). Le classi sono "gusci" che leggono dati da file JSON.

    PATTERN FLYWEIGHT: La memoria RAM gestisce solo gli oggetti visibili a schermo (viewport verticale).

    SISTEMA 16-DIR: Navigazione basata su 16 direzioni (step di 22.5 gradi).

    MOTORE D20: Ogni interazione (1-20) definisce Fallimento Critico (1) o Successo Critico (20).

    MULTIPLO DI 1600: Ogni categoria (Nemici, Item, Luoghi, NPC, Eventi) è tarata su 1600 istanze per mantenere la coerenza della mappa 16x1000.

3. REGOLE PER IL CODICE

    Utilizzo di Classi Python (OOP).

    Metodi per il calcolo delle statistiche dinamiche (Level Scaling).

    Integrazione obbligatoria del sistema "Elementi" (Entropia, Gravità, Psiche, Alchimia, Risonanza).