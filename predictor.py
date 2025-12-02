from concurrent.futures import ThreadPoolExecutor
from inference_sdk import InferenceHTTPClient
import requests

from constants import *
import utils

class Predictor:

    def __init__(self, cv_class):
        
        self.detect_elixir = detect_elixir
        self.detect_card = cv_class.detect_card
        self.detect_field = cv_class.detect_field
        self.detect_ally_tower = detect_ally_tower
        self.detect_enemy_tower = detect_enemy_tower

    def get_predictions_async(self, screen_crops):
        elixir_crop = screen_crops[KEY_ELIXIR]
        cards_crop = screen_crops[KEY_CARDS]
        next_card_crop = screen_crops[KEY_NEXT_CARD]
        field_crop = screen_crops[KEY_FIELD]
        ally_king_crop = screen_crops[KEY_ALLY_KING]
        ally_princesses_crop = screen_crops[KEY_ALLY_PRINCESSES]
        enemy_king_crop = screen_crops[KEY_ENEMY_KING]
        enemy_princesses_crop = screen_crops[KEY_ENEMY_PRINCESSES]

        with ThreadPoolExecutor() as executor:
            # Tasks starten
            future_elixir = executor.submit(self.detect_elixir, elixir_crop)
            futures_cards = [executor.submit(self.detect_card, card) for card in cards_crop]
            future_next_card = executor.submit(self.detect_card, next_card_crop)
            future_field = executor.submit(self.detect_field, field_crop)
            future_ally_king = executor.submit(self.detect_ally_tower, ally_king_crop)
            future_ally_princesses = [executor.submit(self.detect_ally_tower, ally_princess) for ally_princess in ally_princesses_crop]
            future_enemy_king = executor.submit(self.detect_enemy_tower, enemy_king_crop)
            future_enemy_princesses = [executor.submit(self.detect_enemy_tower, enemy_princess) for enemy_princess in enemy_princesses_crop]

            # Ergebnisse einsammeln
            elixir_prediction = future_elixir.result()
            cards_prediction = [f.result() for f in futures_cards]
            next_card_prediction = future_next_card.result()
            field_prediction = future_field.result()
            ally_king_prediction = future_ally_king.result()
            ally_princesses_prediction = [f.result() for f in future_ally_princesses]
            enemy_king_prediction = future_enemy_king.result()
            enemy_princesses_prediction = [f.result() for f in future_enemy_princesses]

        return {
            KEY_ELIXIR: elixir_prediction,
            KEY_CARDS: cards_prediction,
            KEY_NEXT_CARD: next_card_prediction,
            KEY_FIELD: field_prediction
        }

    def get_predictions(self, screen_crops):
        elixir_crop = screen_crops[KEY_ELIXIR]
        cards_crop = screen_crops[KEY_CARDS]
        next_card_crop = screen_crops[KEY_NEXT_CARD]
        field_crop = screen_crops[KEY_FIELD]
        ally_king_crop = screen_crops[KEY_ALLY_KING]
        ally_princesses_crop = screen_crops[KEY_ALLY_PRINCESSES]
        enemy_king_crop = screen_crops[KEY_ENEMY_KING]
        enemy_princesses_crop = screen_crops[KEY_ENEMY_PRINCESSES]

        elixir_prediction = self.detect_elixir(elixir_crop)
        cards_prediction = [self.detect_card(card) for card in cards_crop]
        next_card_prediction = self.detect_card(next_card_crop)
        field_prediction = self.detect_field(field_crop)
        ally_king_prediction = self.detect_ally_tower(ally_king_crop)
        ally_princesses_prediction = [self.detect_ally_tower(tower) for tower in ally_princesses_crop]
        enemy_king_prediction = self.detect_enemy_tower(enemy_king_crop)
        enemy_princesses_prediction = [self.detect_enemy_tower(tower) for tower in enemy_princesses_crop]

        return {
            KEY_ELIXIR: elixir_prediction,
            KEY_CARDS: cards_prediction,
            KEY_NEXT_CARD: next_card_prediction,
            KEY_FIELD: field_prediction
        }

class LocalFlow:

    def __init__(self):
        self.client = InferenceHTTPClient(
                api_url="http://localhost:9001",
                api_key=ROBOFLOW_API_KEY
            )

    def detect_field(self, field_crop):
        result = self.client.run_workflow(
            workspace_name=WORKSPACE_NAME,
            workflow_id=WORKFLOW_FIELD_DETECTION,
            images={
                "image": utils.to_base64(field_crop)
            },
            use_cache=True
        )
        return result
    
    def detect_card(self, card_crop):
        result = self.client.run_workflow(
            workspace_name=WORKSPACE_NAME,
            workflow_id=WORKFLOW_CARD_DETECTION,
            images={
                "image": utils.to_base64(card_crop)
            },
            use_cache=True
        )
        return result

class CloudFlow:

    def detect_field(self, field_crop):
        url = f"https://serverless.roboflow.com/{WORKSPACE_NAME}/workflows/{WORKFLOW_FIELD_DETECTION}"
        payload = {
            "api_key": ROBOFLOW_API_KEY,
            "inputs": {
                "image": {"type": "base64", "value": utils.to_base64(field_crop)}
            }
        }
        response = requests.post(url, json=payload)
        return response.json()

    def detect_card(self, card_crop):
        url = f"https://serverless.roboflow.com/{WORKSPACE_NAME}/workflows/{WORKFLOW_CARD_DETECTION}"
        payload = {
            "api_key": ROBOFLOW_API_KEY,
            "inputs": {
                "image": {"type": "base64", "value": utils.to_base64(card_crop)}
            }
        }
        response = requests.post(url, json=payload)
        return response.json()

def detect_elixir(img_elixir_area):
    pixels = img_elixir_area.load()
    w, h = img_elixir_area.size

    filled_pixels = 0

    for x in range(w):
        r, g, b = pixels[x, 0]
        if (r > 150 and g < 120 and b > 150):
            filled_pixels += 1

    return round(filled_pixels / w, 1)

def detect_ally_tower(img_tower_area):
    pixels = img_tower_area.load()
    w, h = img_tower_area.size

    filled_pixels = 0
    for x in range(w):
        r, g, b = pixels[x, 0]
        if ((r > 85 and g > 120 and b > 120)):
            filled_pixels += 1
    return round(filled_pixels / w, 4)

def detect_enemy_tower(img_tower_area):
    pixels = img_tower_area.load()
    w, h = img_tower_area.size

    filled_pixels = 0
    for x in range(w):
        r, g, b = pixels[x, 0]
        if (r >= 200 and g <= 50):
            filled_pixels += 1
    return round(filled_pixels / w, 4)