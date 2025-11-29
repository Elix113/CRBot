from turtle import width
import pyautogui
import time

import config
import utils

# Relative Positionen in % von der oberen linken Ecke
HEIGHT_FIELD = 81

X_CARDS = 22.1
Y_CARDS = 83
WIDTH_CARD = 18.9
HEIGHT_CARD = 13

X_ELIXIR = 27
Y_ELIXIR = 96.65
WIDTH_ELIXIR = 70.5
HEIGHT_ELIXIR = 2.55

X_NEXT_CARD = 5.5
Y_NEXT_CARD = 93.5
WIDTH_NEXT_CARD = 8.5
HEIGHT_NEXT_CARD = 5.75

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


class ScreenClicker:
    
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