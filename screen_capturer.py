from turtle import width
import pyautogui
import time

import config
import utils
from constants import *

class ScreenCapturer:


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

    @staticmethod
    def load_field():
        c = config.Config()
        if not c.has(config.KEY_FIELD_COORDINATES):
            coords = ScreenCapturer.select_field()
            c.set(config.KEY_FIELD_COORDINATES, coords)
        return c.get(config.KEY_FIELD_COORDINATES)

    @staticmethod
    def take_screenshot(field_coordinates):
        (x1, y1), (x2, y2) = field_coordinates
        width = x2 - x1
        height = y2 - y1
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        return screenshot
   
    # @staticmethod
    # def capture_card_area(field_coordinates):
    #     x = utils.get_abs_x(field_coordinates, X_CARDS)
    #     y = utils.get_abs_y(field_coordinates, Y_CARDS)
    #     width = utils.get_abs_x_distance(field_coordinates, 4*WIDTH_CARD + 3*SPACING_CARDS)
    #     height = utils.get_abs_y_distance(field_coordinates, HEIGHT_CARD)
    #     screenshot = pyautogui.screenshot(region=(x, y, width, height))
    #     return screenshot
    
    @staticmethod
    def get_field_crop(screenshot):
        w, h = screenshot.size
        img_coords = ((0, 0), (w, h))
        field = screenshot.crop((0, 0, w, utils.get_abs_y(img_coords, HEIGHT_FIELD)))
        return field
    
    @staticmethod
    def get_cards_crop(screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_CARDS)
        y = utils.get_abs_y(img_coords, Y_CARDS)
        w = utils.get_abs_x(img_coords, WIDTH_CARD)
        h = utils.get_abs_y(img_coords, HEIGHT_CARD)
        cards = []
        for i in range(4):
            cards.append(screenshot.crop((x+i*w, y, x+w+i*w, y+h)))
        return cards
    
    @staticmethod
    def get_next_card_crop(screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_NEXT_CARD)
        y = utils.get_abs_y(img_coords, Y_NEXT_CARD)
        w = utils.get_abs_x(img_coords, WIDTH_NEXT_CARD)
        h = utils.get_abs_y(img_coords, HEIGHT_NEXT_CARD)
        return screenshot.crop((x, y, x+w, y+h))

    @staticmethod
    def get_elixir_crop(screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_ELIXIR)
        y = utils.get_abs_y(img_coords, Y_ELIXIR)
        w = utils.get_abs_x(img_coords, WIDTH_ELIXIR)
        h = utils.get_abs_y(img_coords, HEIGHT_ELIXIR)
        return screenshot.crop((x, y, x+w, y+h))