import json
import os

def generate_enemy_database(count=1600):
    database = {}
    elements = ["Entropy", "Gravity", "Psyche", "Alchemy", "Resonance"]

    for i in range(count):
        enemy_id = f"enemy_{i}"
        
        # Logica di progressione: le stat aumentano con l'aumentare dell'ID
        level = (i // 16) + 1  # Ogni 16 nemici il livello base sale
        base_hp = 50 + (i * 10)
        base_atk = 10 + (i * 2)
        
        # Selezione elemento ciclica o random
        element = elements[i % len(elements)]

        database[enemy_id] = {
            "metadata": {
                "name": f"Creatura dell'Ombra #{i}",
                "rarity": "Common" if i < 1000 else "Rare" if i < 1500 else "Legendary"
            },
            "stats": {
                "base_level": level,
                "hp": base_hp,
                "atk": base_atk,
                "def": base_atk // 2
            },
            "logic": {
                "primary_element": element,
                "attack_ids": [i, i+1, i+2, i+3, i+4] # Mappa i 5 attacchi per ID
            }
        }

    # Assicurati che la cartella esista
    os.makedirs('data', exist_ok=True)
    
    with open('data/enemies_db.json', 'w') as f:
        json.dump(database, f, indent=2)
    
    print(f"Successo! Generati {count} nemici nel database.")

if __name__ == "__main__":
    generate_enemy_database()