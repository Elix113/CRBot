import time
import pyautogui

from constants import *
import utils


class Actioner:
    
    def __init__(self, field_coordinates: dict[str, int]):
        self.field_coordinates = field_coordinates
        self.card_abs_positions = self.get_cards_positions()

    def place_card(self, card: int, destination_pos):
        qx, qy = self.card_abs_positions[card]
        dx, dy = self.get_abs_pos(destination_pos)
        print(f"Take card {card} @{qx, qy}")
        pyautogui.leftClick(qx, qy)
        time.sleep(2)
        print(f"Place card {card} @{dx, dy}")
        pyautogui.leftClick(dx, dy)

    def get_cards_positions(self):
        card_positions = []
        for i in range(4):
            x = utils.get_abs_x(self.field_coordinates, X_CARDS + WIDTH_CARD/2 + i * WIDTH_CARD)
            y = utils.get_abs_y(self.field_coordinates, Y_CARDS + (HEIGHT_CARD/2))
            card_positions.append((x, y))
        return card_positions