🛠️ Dettagli Tecnici per l'Unificazione

    Ereditarietà Totale: Sia Enemy (in enemies.py) che il Player erediteranno da questa classe. Questo significa che se decidi di aggiungere una nuova statistica (es. "Resilienza alla Risonanza"), ti basterà aggiungerla qui per aggiornare istantaneamente tutte le 3200+ entità del gioco.

    UX Mobile (Visual Feedback): Gli stati alterati (active_statuses) devono essere rappresentati graficamente con piccole icone circolari sopra l'entità. Essendo un gioco verticale, queste icone devono essere leggibili anche quando l'entità è vicina ai bordi.

    Persistenza Cross-Node: Quando il giocatore si muove nel MapSystem, lo stato active_statuses dell'entità viene serializzato nel map_db.json. Se torni indietro dopo 2 turni, il nemico avrà ancora i debuff attivi, ma con la durata ridotta.
    
---

import math

class BaseEntity:
    """
    Classe radice per tutte le entità (Player, Enemy, NPC).
    Gestisce statistiche vitali, stati alterati e interazione con il D20.
    """
    def __init__(self, name, level, base_stats):
        self.name = name
        self.level = level
        
        # Statistiche primarie scalate sul livello
        self.max_hp = base_stats.get("hp", 100) * (1 + (level * 0.1))
        self.current_hp = self.max_hp
        self.max_mana = base_stats.get("mana", 50) * (1 + (level * 0.1))
        self.current_mana = self.max_mana
        
        # Sistema di Stati Alterati Persistenti
        # Struttura: {"status_id": rounds_remaining}
        self.active_statuses = {}
        
        self.is_alive = True
        self.is_stunned = False

    def update_status_effects(self):
        """
        Processa i debuff all'inizio di ogni turno.
        Rende il combattimento complesso e tattico.
        """
        keys_to_remove = []
        for status, duration in self.active_statuses.items():
            # Esempio: Entropia (Danni nel tempo) o Psiche (Confusione)
            self._apply_status_logic(status)
            
            self.active_statuses[status] -= 1
            if self.active_statuses[status] <= 0:
                keys_to_remove.append(status)
        
        for key in keys_to_remove:
            del self.active_statuses[key]

    def _apply_status_logic(self, status):
        """Logica interna per gestire le 5 influenze elementali."""
        if status == "Decadimento_Entropico":
            self.current_hp -= (self.max_hp * 0.05) # Perdi il 5% ogni turno
        elif status == "Pressione_Gravitazionale":
            self.is_stunned = True # Salta il turno se la gravità è troppa

    def take_damage(self, raw_damage, damage_type, dice_roll):
        """
        Metodo universale di ricezione danno.
        Integra il D20 per determinare schivate o blocchi.
        """
        # Se il dado del nemico è un 1 (Fallimento Critico), l'entità schiva
        if dice_roll["is_fail"]:
            return 0
            
        # Calcolo riduzione danno (Base)
        mitigated_damage = max(1, raw_damage - (self.level * 0.5))
        self.current_hp -= mitigated_damage
        
        if self.current_hp <= 0:
            self.current_hp = 0
            self.is_alive = False
            
        return mitigated_damage

    def apply_status(self, status_id, duration):
        """Aggiunge un effetto alterato che persiste tra i nodi della mappa."""
        self.active_statuses[status_id] = duration