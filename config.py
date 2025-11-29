import json
import os
CONFIG_FILE = "config.json"

KEY_FIELD_COORDINATES = "field_cooedinates"

class Config:
    def __init__(self, filepath=CONFIG_FILE):
        self.filepath = filepath
        self.data = {}

        if os.path.exists(filepath):
            self.load()
        else:
            self.save()

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def has(self, key):
        return key in self.data

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    def load(self):
        try:
            with open(self.filepath, "r") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}
            self.save()