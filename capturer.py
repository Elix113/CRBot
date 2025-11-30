from turtle import width
import pyautogui
import time

import config
import utils
from constants import *

class Capturer:

    def __init__(self, game_coordinates):
        self.game_coordinates = game_coordinates

    @staticmethod
    def load_field():
        c = config.Config()
        if not c.has(config.KEY_FIELD_COORDINATES):
            coords = Capturer.select_field()
            c.set(config.KEY_FIELD_COORDINATES, coords)
        return c.get(config.KEY_FIELD_COORDINATES)
    
    @staticmethod
    def select_field():
        print("Bitte bewege die Maus zur oberen linken Ecke des Spielfelds und drücke Enter")
        input("Mit Enter bestätigen...")
        x1, y1 = pyautogui.position()

        print("Bitte bewege die Maus zur unteren rechten Ecke des Spielfelds und drücke Enter")
        input("Mit Enter bestätigen...")
        x2, y2 = pyautogui.position()

        coords = ((x1,y1), (x2,y2))
        print("Field position: ", coords)
        return coords

    def get_all_crops(self, screenshot):
        return {
            "elixir": self.get_elixir_crop(screenshot),
            "cards": self.get_cards_crop(screenshot),
            "next_card": self.get_next_card_crop(screenshot),
            "field": self.get_field_crop(screenshot)
        }

    def take_screenshot(self):
        (x1, y1), (x2, y2) = self.game_coordinates
        width = x2 - x1
        height = y2 - y1
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        return screenshot
   
    def get_elixir_crop(self, screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_ELIXIR)
        y = utils.get_abs_y(img_coords, Y_ELIXIR)
        w = utils.get_abs_x(img_coords, WIDTH_ELIXIR)
        h = utils.get_abs_y(img_coords, HEIGHT_ELIXIR)
        return screenshot.crop((x, y, x+w, y+h))
    
    def get_cards_crop(self, screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_CARDS)
        y = utils.get_abs_y(img_coords, Y_CARDS)
        w = utils.get_abs_x(img_coords, WIDTH_CARD)
        h = utils.get_abs_y(img_coords, HEIGHT_CARD)
        cards = []
        for i in range(4):
            cards.append(screenshot.crop((x+i*w, y, x+w+i*w, y+h)))
        return cards
    
    def get_next_card_crop(self, screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_NEXT_CARD)
        y = utils.get_abs_y(img_coords, Y_NEXT_CARD)
        w = utils.get_abs_x(img_coords, WIDTH_NEXT_CARD)
        h = utils.get_abs_y(img_coords, HEIGHT_NEXT_CARD)
        return screenshot.crop((x, y, x+w, y+h))

    def get_field_crop(self, screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_FIELD)
        y = utils.get_abs_y(img_coords, Y_FIELD)
        w = utils.get_abs_x(img_coords, WIDTH_FIELD)
        h = utils.get_abs_y(img_coords, HEIGHT_FIELD)
        field = screenshot.crop((x, y, x+w, y+h))
        return field