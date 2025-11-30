from ast import List
import numpy as np
import json
import re

from constants import *

with open("card_map.json", "r", encoding="utf-8") as f:
    CARD_MAP = json.load(f)

class State:

    def __init__(self, elixir_prediction, cards_prediction, nextcard_prediction, field_prediction, field_size):
        self.elixir: float = 0.0
        self.cards: List[float] = [0.0, 0.0, 0.0, 0.0]
        self.next_card: float = 0.0
        self.ally_towers: List[float] = [0.0, 0.0, 0.0]
        self.enemy_towers: List[float] = [0.0, 0.0, 0.0]
        self.field = np.zeros((STATE_FIELD_MTRX_H, STATE_FIELD_MTRX_W))
        self.field_w, self.field_h = field_size

        self.set_elixir(elixir_prediction)
        self.set_cards(cards_prediction)
        self.set_next_card(nextcard_prediction)
        self.set_field(field_prediction)

    def set_elixir(self, elixir):
        self.elixir = elixir
    
    def set_cards(self, cards_prediction):
        for i, data in enumerate(cards_prediction):
            if (data[0]["predictions"]["predictions"]):
                card_class = data[0]["predictions"]["predictions"][0]["class"]
                self.cards[i] = self.card_to_id(card_class)
    
    def set_next_card(self, data):
        if (data[0]["predictions"]["predictions"]):
            card_class = data[0]["predictions"]["predictions"][0]["class"]
            self.next_card = self.card_to_id(card_class)

    def set_field(self, data):
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
                x, y = self.get_matrix_coords(unit["x"], unit["y"])
                self.field[x][y] = 0.1
            elif (unit_class == "ally building"):
                x, y = self.get_matrix_coords(unit["x"], unit["y"])
                self.field[x][y] = 0.2
            elif (unit_class == "ally troop"):
                x, y = self.get_matrix_coords(unit["x"], unit["y"])
                self.field[x][y] = -0.1
            elif (unit_class == "ally building"):
                x, y = self.get_matrix_coords(unit["x"], unit["y"])
                self.field[x][y] = -0.2

    def card_to_id(self, card):
        card = card.lower()
        card = re.sub(r'[^a-z0-9]', '', card)
        card_id = CARD_MAP.get(card, 0)
        return round(card_id / 1000, 3)

    def get_matrix_coords(self, x, y):
        matrix_x = int(y / self.field_h * (STATE_FIELD_MTRX_H-1))
        matrix_y = int(x / self.field_w * (STATE_FIELD_MTRX_W-1))
        return (matrix_x, matrix_y)

    def to_vector(self, old_vector):
        vector = [
            self.elixir,
            *self.cards,
            self.next_card,
            *self.ally_towers,
            *self.enemy_towers,
            *self.field.flatten().tolist()
        ]

        if (old_vector != None):
            for i in range(1, ELIXIR_VECTOR + CARDS_VECTOR + NEXT_CARD_VECTOR + ALLY_TOWER_VECTOR + ENEMY_TOWER_VECTOR):
                if (vector[i] < 1e-6):
                    vector[i] = old_vector[i]

        return vector

    def calculate_reward(self, old_state_vector, state_vector):
        elixir_start = 0
        cards_start = elixir_start + ELIXIR_VECTOR
        next_card_start = cards_start + CARDS_VECTOR
        ally_tower_start = next_card_start + NEXT_CARD_VECTOR
        enemy_tower_start = ally_tower_start + ALLY_TOWER_VECTOR
        field_start = enemy_tower_start + ENEMY_TOWER_VECTOR
        field_end = field_start + STATE_FIELD_MTRX_H * STATE_FIELD_MTRX_W

        reward = 0

        #Eigener Turm verloren
        own_tower_loss = sum(old_state_vector[ally_tower_start:enemy_tower_start]) - sum(state_vector[ally_tower_start:enemy_tower_start])
        reward -= own_tower_loss * 0.5

        #Gegnerische Türme
        enemy_tower_loss = sum(old_state_vector[enemy_tower_start:field_start]) - sum(state_vector[enemy_tower_start:field_start])
        reward += enemy_tower_loss * 1.0

        #Summe der Ally-Truppen (+) vs Gegner-Truppen (-)
        old_field_sum = sum(old_state_vector[field_start:field_end])
        new_field_sum = sum(state_vector[field_start:field_end])
        delta_field = new_field_sum - old_field_sum
        reward += delta_field * 0.01

        return max(min(reward, 1.0), -1.0)

    def to_string(self):
        print("Elixir:      ", self.elixir)
        print("Cards:       ", self.cards)
        print("Next Card:   ", self.next_card)
        print("Ally Towers: ", self.ally_towers)
        print("Enemy Towers:", self.enemy_towers)
        print("Enemy Towers:", self.enemy_towers)
        print("Field:")
        for row in self.field:
            print("             ", row)