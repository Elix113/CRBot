import time
import pyautogui

from constants import *
import utils


class Actioner:
    
    def __init__(self, game_coordinates: dict[str, int]):
        self.game_coordinates = game_coordinates
        self.card_abs_positions = self.get_cards_positions()

    def act(self, action):
        positions_per_card = ACTION_FIELD_MTRX_H * ACTION_FIELD_MTRX_W
        card = action // positions_per_card
        pos = action % positions_per_card
        self.place_card(card, pos)

    def action_to_rel_pos (pos):
        row = pos // ACTION_FIELD_MTRX_W
        col = pos % ACTION_FIELD_MTRX_W
        x = col / (ACTION_FIELD_MTRX_W - 1)
        y = row / (ACTION_FIELD_MTRX_H - 1)
        return x, y

    def place_card(self, card, dest_rel_pos):
        qx, qy = self.card_abs_positions[card]
        dx, dy = self.get_abs_pos(dest_rel_pos)
        print(f"Take card {card} @{qx, qy}")
        pyautogui.leftClick(qx, qy)
        time.sleep(2)
        print(f"Place card {card} @{dx, dy}")
        pyautogui.leftClick(dx, dy)

    def get_cards_positions(self):
        card_positions = []
        for i in range(4):
            x = utils.get_abs_x(self.game_coordinates, X_CARDS + WIDTH_CARD/2 + i * WIDTH_CARD)
            y = utils.get_abs_y(self.game_coordinates, Y_CARDS + (HEIGHT_CARD/2))
            card_positions.append((x, y))
        return card_positions