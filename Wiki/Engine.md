🛠️ Dettagli Tecnici per l'Engine

    State Machine: L'uso della variabile self.current_state è fondamentale per la UX mobile. Impedisce al giocatore di attaccare mentre si sta muovendo o di muoversi durante un dialogo, evitando conflitti di input touch.

    Il Loop dei 1600: L'engine non "conosce" i nemici o gli item. Riceve solo ID e delega ai rispettivi Manager (EnemyManager, ItemFactory) il compito di caricare i dati. Questo mantiene l'Engine leggero e veloce.

    UX Smartphone (Visualizza e Conferma): In un sistema a turni verticale, l'engine deve inviare alla UI i dati per i "Pop-up di conferma". Se il giocatore clicca su un attacco, l'engine risponde con il calcolo del danno potenziale e aspetta il secondo tap per confermare (prevenendo errori).
    
---

class GameEngine:
    """
    Il 'Cervello' del gioco. Coordina il movimento, il combattimento 
    e l'interazione tra i sistemi (D20, Mappa, Inventario).
    """
    def __init__(self, player, map_system, dice_engine):
        self.player = player
        self.map_system = map_system
        self.dice = dice_engine
        self.current_state = "EXPLORATION" # Stati: EXPLORATION, COMBAT, DIALOGUE, MENU
        self.current_enemy = None

    def process_input(self, action_type, payload):
        """
        Punto di ingresso unico per gli input dello smartphone.
        action_type: 'MOVE', 'ATTACK', 'USE_ITEM', 'INTERACT'
        """
        if self.current_state == "EXPLORATION" and action_type == "MOVE":
            return self._handle_movement(payload) # payload è l'indice della direzione (0-15)
        
        elif self.current_state == "COMBAT" and action_type == "ATTACK":
            return self._handle_combat_turn(payload) # payload è l'ID dell'attacco
            
        return {"status": "idle"}

    def _handle_movement(self, direction):
        """Coordina lo spostamento e la generazione di eventi/nemici."""
        move_result = self.map_system.move(direction)
        
        if move_result["status"] == "success":
            # Dopo ogni movimento riuscito, il D20 decide se c'è un incontro (1600 nemici)
            encounter_roll = self.dice.roll()
            
            if encounter_roll["total"] > 15: # Soglia incontro casuale
                self.current_state = "COMBAT"
                return {"event": "ENCOUNTER_START", "pos": move_result["pos"]}
            
            return {"event": "MOVED", "pos": move_result["pos"]}
        
        return move_result

    def _handle_combat_turn(self, attack_id):
        """
        Gestisce la logica dei turni. 
        1. Giocatore agisce -> 2. Controllo stati -> 3. Nemico agisce -> 4. Controllo vittoria
        """
        combat_log = []

        # 1. Fase Giocatore
        player_roll = self.dice.roll(modifier=self.player.level)
        damage = self.player.execute_attack(self.current_enemy, attack_id, player_roll)
        combat_log.append(f"Hai inflitto {damage} danni.")

        # 2. Controllo Morte Nemico
        if not self.current_enemy.is_alive:
            self.current_state = "EXPLORATION"
            loot = self._generate_loot()
            return {"event": "VICTORY", "log": combat_log, "loot": loot}

        # 3. Fase Nemico (IA Semplice)
        enemy_roll = self.dice.roll()
        enemy_dmg = self.current_enemy.take_action(self.player, enemy_roll)
        combat_log.append(f"Il nemico risponde: {enemy_dmg} danni.")

        # 4. Update Stati Alterati (Persistenza Entropica/Psiche)
        self.player.update_status_effects()
        self.current_enemy.update_status_effects()

        return {"event": "TURN_END", "log": combat_log}

    def _generate_loot(self):
        """Usa il D20 per pescare dai 1600 item del database."""
        roll = self.dice.roll()
        # Logica di selezione item_id basata sul roll
        return f"Item_ID_{roll['total'] * 80}" # Esempio di mapping verso i 1600 item