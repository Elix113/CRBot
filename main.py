import os
from dotenv import load_dotenv
import json
from agent import CloudAgent, LocalAgent
import agent
from screen_capturer import ScreenCapturer, ScreenClicker
import state
import utils

# Variablen aus .env lesen
load_dotenv()
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
WORKSPACE = os.getenv("WORKSPACE")
WORKFLOW_FIELD_DETECTION = os.getenv("WORKFLOW_FIELD_DETECTION")
WORKFLOW_CARD_DETECTION = os.getenv("WORKFLOW_CARD_DETECTION")
