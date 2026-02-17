🛠️ Dettagli Tecnici per i 1600 Consumabili

    Gestione del "Drop" (1600 tipologie): La probabilità di trovare uno specifico item tra i 1600 è gestita dal D20 di dice.py. Gli ID da 0-400 sono comuni (erbe), 401-1200 rari (pozioni alchemiche), 1201-1600 unici (oggetti di missione).

    Sinergia con GravitySystem: Il valore restituito da calculate_gravity_penalty() viene passato direttamente alla logica di movimento. Se porti troppe "Chiavi di Ferro" (item pesanti), saltare tra i nodi della mappa diventa più difficile e richiede tiri di dado più alti.

    UX Mobile (Drag & Drop): In un'interfaccia verticale, i consumabili dovrebbero essere accessibili tramite una "Quick-Bar" a scomparsa sul lato dello schermo. Uno swipe verso l'alto sull'icona dell'item lo "usa" istantaneamente, uno swipe verso il basso lo "scarta" per alleggerire il peso.

---

import math

class Consumable:
    """
    Rappresenta uno dei 1600 item consumabili (pozioni, chiavi, mana, etc.).
    Implementa la meccanica del Peso Gravitazionale.
    """
    def __init__(self, item_id, data):
        self.id = item_id
        self.name = data["name"]
        self.type = data["type"] # 'healing', 'mana', 'utility', 'key'
        
        # Statistiche di efficacia
        self.power = data["power"]
        
        # Meccanica Gravità: il peso influenza il movimento verticale
        self.weight = data.get("weight", 1.0)
        
        # Moltiplicatore Alchemico (Bonus se usato in zone Alchimia)
        self.alchemical_potency = 1.0

    def use(self, target, current_biome_element):
        """
        Applica l'effetto dell'item al target.
        """
        potency = self.power
        
        # Bonus Alchimia: se l'ambiente è favorevole, l'item è più potente
        if current_biome_element == "Alchemy":
            potency *= 1.5
            
        if self.type == "healing":
            target.hp = min(target.max_hp, target.hp + potency)
        elif self.type == "mana":
            target.mana = min(target.max_mana, target.mana + potency)
            
        return {"status": "used", "effect": potency}

class ConsumableManager:
    """
    Gestore per la creazione e il bilanciamento dei 1600 consumabili.
    """
    def __init__(self, dice_engine):
        self.dice = dice_engine
        self.total_inventory_weight = 0.0

    def generate_item(self, item_id, global_item_db):
        """
        Istanzia un item dal database dei 1600 oggetti.
        """
        item_data = global_item_db.get(item_id)
        if not item_data:
            return None
            
        return Consumable(item_id, item_data)

    def calculate_gravity_penalty(self):
        """
        Calcola quanto il peso degli oggetti rallenta il giocatore.
        UX: Un peso eccessivo rende i controlli meno reattivi (lentezza verticale).
        """
        if self.total_inventory_weight > 50.0: # Soglia di sovraccarico
            return (self.total_inventory_weight - 50.0) * 0.05
        return 0.0