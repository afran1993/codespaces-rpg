🛠️ Dettagli Tecnici per i 1600 NPC

    Sincronizzazione 16-Direzioni: Se il giocatore approccia un NPC da una direzione specifica (es. "Alle spalle"), il NPCManager può attivare un tiro di dado furtività per permettere un'azione di borseggio o un attacco a sorpresa.

    Il sistema delle "1600 Verità": In un RPG complesso, ogni NPC possiede un frammento di informazione legato a uno dei 1600 luoghi. Questo crea un gameplay investigativo.

    UX Mobile: Il sistema di dialogo utilizza un "Radial Menu" (menu radiale) sovrapposto all'NPC. Questo permette di scegliere tra "Parla", "Scambia", "Attacca" o "Quest" con un unico movimento circolare del pollice.


---


class NPC:
    """
    Rappresenta uno dei 1600 NPC del mondo.
    Gestisce la logica di dialogo, il commercio e le missioni (quest).
    """
    def __init__(self, npc_id, data, local_element):
        self.id = npc_id
        self.name = data["name"]
        self.role = data["role"] # Es: Mercante, Guardiano, Saggio
        self.base_dialogue = data["dialogue_root"]
        self.local_element = local_element # L'elemento del nodo influenza l'umore
        
        # Stato della relazione (Psiche)
        self.disposition = 50 # Da 0 (Ostile) a 100 (Alleato)
        self.has_quest = data.get("has_quest", False)

    def interact(self, player_stats, dice_engine):
        """
        Inizia un'interazione basata sulla Psiche e sul D20.
        """
        # Tiro di dado per vedere se l'NPC è disposto a parlare o commerciare
        roll = dice_engine.roll(modifier=player_stats.get("charisma", 0))
        
        if roll["is_fail"] or self.disposition < 20:
            return f"{self.name} ti guarda con sospetto e si rifiuta di parlare."
        
        if self.local_element == "Psyche":
            # Bonus elementale: in zone Psiche gli NPC rivelano segreti (Lore)
            return f"{self.name} sussurra: 'Sento i tuoi pensieri... prendi questo segreto.'"

        return self.base_dialogue

class NPCManager:
    """
    Gestore per il caricamento e lo spawn dei 1600 NPC.
    """
    def __init__(self, dice_engine):
        self.dice = dice_engine

    def spawn_npc_in_node(self, node_data, global_npc_db):
        """
        Controlla se in un nodo della mappa deve apparire un NPC.
        """
        npc_id = node_data.get("npc_id")
        if not npc_id:
            return None

        # Caricamento Flyweight dal database
        npc_static_data = global_npc_db.get(npc_id)
        
        return NPC(
            npc_id, 
            npc_static_data, 
            node_data.get("local_element")
        )