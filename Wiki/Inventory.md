🛠️ Dettagli Tecnici per l'Inventario

    Sinergia con MapSystem: Quando il giocatore tenta di muoversi in una delle 16 direzioni, il MapSystem interroga inventory.get_gravity_modifier(). Se il valore è alto (>1.5), il tiro del D20 subisce un malus pesante (es. -5 sul totale).

    Ottimizzazione della Lista (UI Verticale): Con 1600 item potenziali, la classe implementa metodi di filtraggio rapido (sort_by_element). Questo permette alla UI dello smartphone di renderizzare solo piccoli gruppi di oggetti alla volta, evitando lag nello scorrimento.

    Persistenza: Questa classe sarà il cuore del sistema di salvataggio. Ogni volta che viene modificata, genera un hash dello stato per garantire che il giocatore non possa "duplicare" item rari manipolando il peso.

---

class Inventory:
    """
    Gestore centralizzato per le 320 armi e i 1600 consumabili.
    Coordina il peso totale e l'interazione con il sistema di Gravità.
    """
    def __init__(self, capacity_limit=50.0):
        # Liste separate per gestire la scalabilità (Flyweight)
        self.weapons = []      # Max 320 tipi possibili
        self.consumables = []  # Max 1600 tipi possibili
        
        self.capacity_limit = capacity_limit
        self.current_weight = 0.0
        self.is_overburdened = False

    def add_item(self, item):
        """
        Aggiunge un oggetto e aggiorna istantaneamente il peso del giocatore.
        """
        item_weight = getattr(item, 'weight', 0.0)
        
        # Logica di aggiunta basata sul tipo di classe
        from items.gear import Weapon
        if isinstance(item, Weapon):
            self.weapons.append(item)
        else:
            self.consumables.append(item)
            
        self.current_weight += item_weight
        self._check_encumbrance()
        return True

    def remove_item(self, item):
        """Rimuove un oggetto e alleggerisce il carico."""
        if item in self.weapons:
            self.weapons.remove(item)
        elif item in self.consumables:
            self.consumables.remove(item)
        else:
            return False

        self.current_weight -= getattr(item, 'weight', 0.0)
        self._check_encumbrance()
        return True

    def _check_encumbrance(self):
        """Aggiorna lo stato di sovraccarico."""
        self.is_overburdened = self.current_weight > self.capacity_limit

    def get_gravity_modifier(self):
        """
        Ritorna un moltiplicatore di penalità per il MapSystem e l'AttackSystem.
        Se sovraccarico, la velocità verticale e la precisione calano.
        """
        if not self.is_overburdened:
            return 1.0
        # Penalità proporzionale all'eccesso di peso
        penalty = (self.current_weight / self.capacity_limit)
        return round(penalty, 2)

    def sort_by_element(self, element_name):
        """
        UX: Permette di filtrare i 1600 item per affinità elementale.
        Esempio: mostra solo item di 'Alchimia' per riparare armi.
        """
        return [i for i in self.consumables if getattr(i, 'element', '') == element_name]