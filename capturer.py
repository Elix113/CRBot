from turtle import width
import pyautogui
import pygetwindow as gw    
import win32gui

import time

import config
import utils
from constants import *

class Capturer:

    def __init__(self, game_coordinates):
        self.game_coordinates = game_coordinates

    def detect_game_coordinates():
        win = gw.getWindowsWithTitle("Clash Royale")[0]
        hwnd = win._hWnd
        client_rect = win32gui.GetClientRect(hwnd)
        top_left = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))
        bottom_right = win32gui.ClientToScreen(hwnd, (client_rect[2], client_rect[3]))
        print("Game Coordinates detected:", top_left, bottom_right)
        return (top_left, bottom_right)


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
            KEY_ELIXIR: self.get_elixir_crop(screenshot),
            KEY_CARDS: self.get_cards_crop(screenshot),
            KEY_NEXT_CARD: self.get_next_card_crop(screenshot),
            KEY_FIELD: self.get_field_crop(screenshot),
            KEY_ALLY_KING: self.get_ally_king_crop(screenshot),
            KEY_ALLY_PRINCESSES: self.get_ally_princesses_crop(screenshot),
            KEY_ENEMY_KING: self.get_enemy_king_crop(screenshot),
            KEY_ENEMY_PRINCESSES: self.get_enemy_princesses_crop(screenshot)
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
        return screenshot.crop((x, y, x+w, y+1))
    
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

    def get_ally_king_crop(self, screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_KING)
        y = utils.get_abs_y(img_coords, Y_ALLY_KING)
        w = utils.get_abs_x(img_coords, WIDTH_KING)
        return screenshot.crop((x, y, x+w, y+1))
    
    def get_ally_princesses_crop(self, screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_LEFT_PRINCESS)
        y = utils.get_abs_y(img_coords, Y_ALLY_PRINCESS)
        w = utils.get_abs_x(img_coords, WIDTH_PRINCESS)
        princesses = []
        for i in range(2):
            princesses.append(screenshot.crop((x, y, x+w, y+1)))
            x = utils.get_abs_x(img_coords, X_RIGHT_PRINCESS)
        return princesses

    def get_enemy_king_crop(self, screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_KING)
        y = utils.get_abs_y(img_coords, Y_ENEMY_KING)
        w = utils.get_abs_x(img_coords, WIDTH_KING)
        return screenshot.crop((x, y, x+w, y+1))

    def get_enemy_princesses_crop(self, screenshot):
        img_coords = ((0, 0), screenshot.size)
        x = utils.get_abs_x(img_coords, X_LEFT_PRINCESS)
        y = utils.get_abs_y(img_coords, Y_ENEMY_PRINCESS)
        w = utils.get_abs_x(img_coords, WIDTH_PRINCESS)
        princesses = []
        for i in range(2):
            princesses.append(screenshot.crop((x, y, x+w, y+1)))
            x = utils.get_abs_x(img_coords, X_RIGHT_PRINCESS)
        return princesses
