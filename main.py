from actioner import Actioner
from agent import DQNAgent
from constants import *
from predictor import Predictor, LocalFlow
from capturer import Capturer
from state import State
import keyboard


def main():

    capturer = Capturer(Capturer.load_field())
    predictor = Predictor(LocalFlow())
    agent = DQNAgent(STATE_VECTOR_LENGTH, ACTION_SIZE)
    agent.load()
    actioner = Actioner(capturer.game_coordinates)

    first_round = True
    done = False
    old_state_vector = None
    reward = None

    start()
    print("x drücken um zu stoppen")
    while not done:
        screenshot = capturer.take_screenshot()
        screen_crops = capturer.get_all_crops(screenshot)
        predictions = predictor.get_predictions_async(screen_crops, True)
        state = State(
            predictions[KEY_ELIXIR], 
            predictions[KEY_CARDS], 
            predictions[KEY_NEXT_CARD], 
            predictions[KEY_FIELD], 
            screen_crops[KEY_FIELD].size
        )
        state_vector = state.to_vector(old_state_vector)

        if (not first_round):
            reward = state.calculate_reward(old_state_vector, state_vector)
            agent.remember(old_state_vector, action, reward, state_vector, done)
            agent.replay() 

        action = agent.act(state_vector)

        actioner.act(action)


        old_state_vector = state_vector
        first_round = False
        done = stop()

    agent.save()

def start():
    input("Start? Mit Enter bestätigen...")

def stop():
    return keyboard.is_pressed("x")

main()
