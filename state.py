from ast import Dict, List
import json
import re

with open("card_map.json", "r", encoding="utf-8") as f:
    CARD_MAP = json.load(f)

class State:

    def __init__(self, elixir_prediction, cards_prediction, nextcard_prediction, field_prediction):
        self.elixir: float = 0
        self.cards: List[int] = []
        self.next_card: int = 0
        self.ally_towers: List[int] = [1, 1, 1]
        self.enemy_towers: List[int] = [1, 1, 1]
        self.ally_troops: List[Dict] = []
        self.enemy_troops: List[Dict] = []

        self.set_elixir(elixir_prediction)
        self.set_cards(cards_prediction)
        self.set_next_card(nextcard_prediction)
        self.set_field(field_prediction)

    def set_elixir(self, elixir):
        self.elixir = elixir
    
    def set_cards(self, cards_prediction):
            self.cards = []
            for data in cards_prediction:
                if (not data[0]["predictions"]["predictions"]):
                    raise ValueError("card could not be detected")
                card_class = data[0]["predictions"]["predictions"][0]["class"]
                self.cards.append(self.card_to_int(card_class))
    
    def set_next_card(self, data):
        if (not data[0]["predictions"]["predictions"]):
                    raise ValueError("next_card could not be detected")
        card_class = data[0]["predictions"]["predictions"][0]["class"]
        self.next_card = self.card_to_int(card_class)

    def set_field(self, data):
        self.ally_troops = []
        self.enemy_troops = []
        predictions = data[0]["predictions"]["predictions"]
        ally_princess = False
        enemy_princess = False

        for unit in predictions:
            unit_class = unit["class"] 
            if (unit_class == "ally king tower"):
                self.ally_towers[1] = 1
            elif (unit_class == "ally princess tower"):
                self.ally_towers[0 if not ally_princess else 2] = 1
                ally_princess = True
            elif (unit_class == "enemy king tower"):
                self.enemy_towers[1] = 1
            elif (unit_class == "enemy princess tower"):
                self.enemy_towers[0 if not enemy_princess else 2] = 1
                enemy_princess = True
            elif (unit_class == "ally troop"):
                self.ally_troops.append({
                        "x": unit["x"],
                        "y": unit["y"],
                })
            elif (unit_class == "enemy troop"):
                self.enemy_troops.append({
                        "x": unit["x"],
                        "y": unit["y"],
                })

    def card_to_int(self, card):
        card = card.lower()
        card = re.sub(r'[^a-z0-9]', '', card)
        return CARD_MAP.get(card, -1)

    def to_string(self):
        print("Elixir:      ", self.elixir)
        print("Cards:       ", self.cards)
        print("Next Card:   ", self.next_card)
        print("Ally Towers: ", self.ally_towers)
        print("Enemy Towers:", self.enemy_towers)
        print("Ally Troops: ", self.ally_troops)
        print("Enemy Troops:", self.enemy_troops)