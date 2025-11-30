import os
from dotenv import load_dotenv
import json

import torch
from agent import DQNAgent
from predictor import LocalFlow
from capturer import Capturer
from state import State

# Variablen aus .env lesen
load_dotenv()
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
WORKSPACE = os.getenv("WORKSPACE")
WORKFLOW_FIELD_DETECTION = os.getenv("WORKFLOW_FIELD_DETECTION")
WORKFLOW_CARD_DETECTION = os.getenv("WORKFLOW_CARD_DETECTION")

def main():

    screen_capturer = Capturer()
    roboflow = LocalFlow(ROBOFLOW_API_KEY, WORKSPACE, WORKFLOW_FIELD_DETECTION, WORKFLOW_CARD_DETECTION)
    old_vector = None

    state = update_state(screen_capturer, roboflow, old_vector)

def update_state(screen_capturer, roboflow, old_vector):
    #Informationen vom Screen holen
    screenshot = screen_capturer.take_screenshot()
    elixir_crop = screen_capturer.get_elixir_crop(screenshot)
    cards_crop = screen_capturer.get_cards_crop(screenshot)
    next_card_crop = screen_capturer.get_next_card_crop(screenshot)
    field_crop = screen_capturer.get_field_crop(screenshot)

    #Predictions holen
    elixir_prediction = roboflow.get_elixir(elixir_crop)
    cards_prediction = []
    for card in cards_crop:
        cards_prediction.append(roboflow.detect_card(card))
    next_card_prediction = roboflow.detect_card(next_card_crop)
    field_prediction = roboflow.detect_field(field_crop)

    #State erstellen
    state = State(elixir_prediction, cards_prediction, next_card_prediction, field_prediction, field_crop.size)
    return state.to_vector(old_vector)

main()
