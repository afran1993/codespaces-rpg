import random

class DiceSystem:
    """
    Sistema di probabilità centrale basato su D20.
    Gestisce il calcolo del successo per eventi, attacchi e check statistici.
    """
    def __init__(self, sides=20):
        self.sides = sides

    def roll(self, modifier=0):
        """
        Esegue un tiro di dado.
        :param modifier: Bonus o malus derivante da statistiche/equipaggiamento.
        :return: Un dizionario con il risultato grezzo e il tipo di successo.
        """
        raw_roll = random.randint(1, self.sides)
        total = raw_roll + modifier
        
        # Logica per i successi critici (tipica degli RPG complessi)
        is_critical_success = (raw_roll == 20)
        is_critical_fail = (raw_roll == 1)
        
        return {
            "raw": raw_roll,
            "total": total,
            "is_crit": is_critical_success,
            "is_fail": is_critical_fail
        }

    def check_event(self, threshold):
        """
        Verifica se un evento con una determinata difficoltà (threshold) avviene.
        Utile per i 1600 eventi casuali.
        """
        result = self.roll()
        return result["total"] >= threshold