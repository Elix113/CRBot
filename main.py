import os
from dotenv import load_dotenv
import json

import torch
from agent import DQNAgent
from constants import *
from predictor import Predictor, LocalFlow
from capturer import Capturer
from state import State

def main():

    capturer = Capturer(Capturer.load_field())
    screen_crops = capturer.get_all_crops()

    predictor = Predictor(LocalFlow())
    predictions = predictor.get_predictions(screen_crops, True)

    state = State(
        predictions[KEY_ELIXIR], 
        predictions[KEY_CARDS], 
        predictions[KEY_NEXT_CARD], 
        predictions[KEY_FIELD], 
        screen_crops[KEY_FIELD].size
    )

    print(state.to_vector(None))

main()
