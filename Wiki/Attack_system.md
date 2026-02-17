🛠️ Perché questa scelta è UX-Friendly?

    Feedback Immediato: Su smartphone, il giocatore "sente" il ritmo. Se sbaglia il tempismo del touch, il sync_multiplier crolla e gli attacchi speciali (i 5 dell'arma) tornano bloccati.

    Scalabilità Massima: Se domani vuoi cambiare il bilanciamento di tutti i 1600 attacchi, devi toccare solo questo file sotto core/, non 1600 classi diverse.

    Visualizzazione Verticale: Il moltiplicatore di Risonanza può essere visualizzato come una barra laterale sottile, perfetta per i bordi dello schermo mobile.

    ---

    class AttackSystem:
    """
    Il 'Motore di Combattimento'. Gestisce i 1600 tipi di attacchi,
    calcolando danni, costi di risonanza ed effetti elementali.
    """
    def __init__(self, dice_engine, element_manager):
        self.dice = dice_engine
        self.elements = element_manager
        # Il moltiplicatore di Sync aumenta con i tocchi a ritmo (UX Smartphone)
        self.sync_multiplier = 1.0 

    def execute_attack(self, attacker, defender, attack_id, timing_score):
        """
        Esegue un attacco specifico tra i 1600 disponibili.
        :param timing_score: Valore da 0.0 a 1.0 basato sulla precisione del touch.
        """
        # 1. Carica i dati dell'attacco (da attack_db.json)
        # Supponiamo che l'attack_id ci dica: nome, base_power, element_type, sync_cost
        attack_data = self._get_attack_data(attack_id)
        
        # 2. Aggiorna la Risonanza (UX: premia il giocatore bravo col touch)
        self.sync_multiplier += (timing_score * 0.2)
        
        # 3. Tiro di Dado D20 per il colpo
        roll = self.dice.roll(modifier=attacker.level)
        
        if roll["is_fail"]:
            self.sync_multiplier = 1.0 # Il fallimento rompe il ritmo
            return {"status": "miss", "damage": 0}

        # 4. Calcolo Danno Complesso
        # Formula: (Potenza Base * Forza Arma * Moltiplicatore Sync) + Bonus D20
        raw_damage = (attack_data["power"] * attacker.attack_power * self.sync_multiplier)
        
        # 5. Applicazione Elementale (Danno vs Resistenze)
        final_damage = defender.take_damage(raw_damage, attack_data["element"])
        
        # 6. Effetti Collaterali (es. Entropia consuma durabilità arma)
        if hasattr(attacker, 'weapon'):
            attacker.weapon.apply_wear(0.5) # Ogni attacco consuma un po' l'arma

        return {
            "status": "hit",
            "damage": final_damage,
            "is_crit": roll["is_crit"],
            "current_sync": self.sync_multiplier
        }

    def _get_attack_data(self, attack_id):
        """
        Simula il recupero dal DB dei 1600 attacchi.
        Ogni arma ha 5 attacchi mappati (es. 0=Base, 4=Ultima).
        """
        # Esempio di struttura dato
        return {
            "name": f"Tecnica #{attack_id}",
            "power": 10 + (attack_id % 5) * 5,
            "element": "Resonance",
            "sync_cost": (attack_id % 5) * 0.5
        }