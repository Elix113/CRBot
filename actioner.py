import time
import pyautogui

from constants import *
import utils


class Actioner:
    
    def __init__(self, game_coordinates):
        self.game_coordinates = game_coordinates

    def act(self, action, do=True):
        if (action == ACTION_SIZE-1):
            return (-1, -1)
        positions_per_card = ACTION_FIELD_MTRX_H * ACTION_FIELD_MTRX_W
        card = action // positions_per_card
        pos = self.action_pos_to_rel_pos(action % positions_per_card)
        if (do):
            self.place_card(card, pos)
        return (card, pos)

    def action_pos_to_rel_pos(self, pos):
        row = pos // ACTION_FIELD_MTRX_W
        col = pos % ACTION_FIELD_MTRX_W
        x = X_FIELD + (col / (ACTION_FIELD_MTRX_W - 1)) * WIDTH_FIELD
        y = Y_FIELD + (row / (ACTION_FIELD_MTRX_H - 1)) * HEIGHT_FIELD
        x = col / (ACTION_FIELD_MTRX_W - 1) * 100
        y = row / (ACTION_FIELD_MTRX_H - 1) * 100
        return (x, y)

    def place_card(self, card, dest_rel_pos):
        qx, qy = self.get_cards_position(card)
        dx, dy = utils.get_abs_pos(self.game_coordinates, dest_rel_pos)
        print(f"Take card {card} @{qx, qy}")
        pyautogui.leftClick(qx, qy)
        print(f"Place card {card} @{dx, dy}")
        pyautogui.leftClick(dx, dy)
        return (dx, dy)

    def get_cards_position(self, card):
        x = utils.get_abs_x(self.game_coordinates, X_CARDS + WIDTH_CARD/2 + card * WIDTH_CARD)
        y = utils.get_abs_y(self.game_coordinates, Y_CARDS + (HEIGHT_CARD/2))
        return (x, y)