import math

class MapSystem:
    """
    Gestisce la navigazione nei 1600 luoghi (16x100) del mondo.
    Implementa il movimento in 16 direzioni e il caricamento dei dati.
    """
    def __init__(self, dice_engine):
        self.dice = dice_engine # Integrazione D20 per incontri casuali
        self.grid_width = 16
        self.grid_height = 100
        self.current_pos = {"x": 0, "y": 0}
        
        # Dizionario delle 16 direzioni (Delta X, Delta Y)
        # Semplificato: le direzioni intermedie richiedono check D20 per successo
        self.directions = {
            0: (0, 1),   1: (1, 2),   2: (1, 1),   3: (2, 1),
            4: (1, 0),   5: (2, -1),  6: (1, -1),  7: (1, -2),
            8: (0, -1),  9: (-1, -2), 10: (-1, -1), 11: (-2, -1),
            12: (-1, 0), 13: (-2, 1), 14: (-1, 1), 15: (-1, 2)
        }

    def move(self, direction_index):
        """
        Tenta di muovere il giocatore in una delle 16 direzioni.
        """
        if direction_index not in self.directions:
            return {"status": "error", "msg": "Direzione invalida"}

        dx, dy = self.directions[direction_index]
        
        new_x = self.current_pos["x"] + dx
        new_y = self.current_pos["y"] + dy

        # Controllo dei confini (Constraint per il formato smartphone)
        if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
            # Check D20: Muoversi in direzioni difficili richiede un tiro di dado
            move_check = self.dice.roll(modifier=2) # Bonus base movimento
            
            if move_check["total"] >= 5: # Soglia minima per non inciampare
                self.current_pos["x"] = new_x
                self.current_pos["y"] = new_y
                return {"status": "success", "pos": self.current_pos, "dice": move_check}
            else:
                return {"status": "failed", "msg": "Terreno impervio, movimento fallito", "dice": move_check}
        
        return {"status": "blocked", "msg": "Confine del regno raggiunto"}

    def get_node_id(self):
        """Converte coordinate in ID per il database JSON"""
        return f"{self.current_pos['x']}_{self.current_pos['y']}"

    def get_local_environment(self, map_data):
        """
        Recupera i dati dei 1600 luoghi dal JSON caricato.
        """
        node_id = self.get_node_id()
        return map_data.get(node_id, {"name": "Terre Ignote", "element": "None"})