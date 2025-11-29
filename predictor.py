from io import BytesIO
from inference_sdk import InferenceHTTPClient
import requests
import base64

import utils

class LocalFlow:

    def __init__(self, api_key, workspace, field_detection, card_detection):
        self.workspace = workspace
        self.field_detection = field_detection
        self.card_detection = card_detection
        self.client = InferenceHTTPClient(
            api_url="http://localhost:9001",
            api_key=api_key
        )

    def detect_field(self, field_crop):
        result = self.client.run_workflow(
            workspace_name=self.workspace,
            workflow_id=self.field_detection,
            images={
                "image": utils.to_base64(field_crop)
            },
            use_cache=True
        )
        return result
    
    def detect_card(self, card_crop):
        result = self.client.run_workflow(
            workspace_name=self.workspace,
            workflow_id=self.card_detection,
            images={
                "image": utils.to_base64(card_crop)
            },
            use_cache=True
        )
        return result

    def get_elixir(self, img_elixir_area):
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

    

class CloudFlow:

    def __init__(self, api_key, workspace, field_detection, card_detection):
        self.api_key = api_key
        self.workspace = workspace
        self.field_detection = field_detection
        self.card_detection = card_detection

    def detect_field(self, field_crop):
        url = f"https://serverless.roboflow.com/{self.workspace}/workflows/{self.field_detection}"
        payload = {
            "api_key": self.api_key,
            "inputs": {
                "image": {"type": "base64", "value": utils.to_base64(field_crop)}
            }
        }
        response = requests.post(url, json=payload)
        return response.json()

    def detect_card(self, card_crop) -> dict:
        url = f"https://serverless.roboflow.com/{self.workspace}/workflows/{self.card_detection}"
        payload = {
            "api_key": self.api_key,
            "inputs": {
                "image": {"type": "base64", "value": utils.to_base64(card_crop)}
            }
        }
        response = requests.post(url, json=payload)
        return response.json()