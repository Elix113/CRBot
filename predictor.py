from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from inference_sdk import InferenceHTTPClient
import requests
import base64

from constants import *
import utils


class Predictor:

    def __init__(self, cv_class):
        
        self.get_elixir = detect_elixir
        self.detect_card = cv_class.detect_card
        self.detect_field = cv_class.detect_field

    def get_predictions(self, screen_crops, cards):
        elixir_crop = screen_crops[KEY_ELIXIR]
        cards_crop = screen_crops[KEY_CARDS]
        next_card_crop = screen_crops[KEY_NEXT_CARD]
        field_crop = screen_crops[KEY_FIELD]

        with ThreadPoolExecutor() as executor:
            # Tasks starten
            future_elixir = executor.submit(self.get_elixir, elixir_crop)
            if (cards):
                futures_cards = [executor.submit(self.detect_card, c) for c in cards_crop]
            future_next_card = executor.submit(self.detect_card, next_card_crop)
            future_field = executor.submit(self.detect_field, field_crop)

            # Ergebnisse einsammeln
            elixir_prediction = future_elixir.result()
            if (cards):
                cards_prediction = [f.result() for f in futures_cards]
            else: 
                cards_prediction = []
            next_card_prediction = future_next_card.result()
            field_prediction = future_field.result()

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

    def detect_card(self, card_crop) -> dict:
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

    filled_columns = 0

    for x in range(w):
        filled_pixels_in_column = 0

        for y in range(h):
            r, g, b = pixels[x, y]
            if ((r > 150 and g < 120 and b > 150) or (r > 200 and g > 200 and b > 200)):
                filled_pixels_in_column += 1

        if filled_pixels_in_column > h * 0.3:
            filled_columns += 1

    return round(filled_columns / w, 1)