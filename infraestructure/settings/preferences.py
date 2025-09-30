import json
import os


class Preferences:
    FILE_PATH = os.path.join(os.path.dirname(__file__), "UserPreferences.json")

    @classmethod
    def save(cls, data: dict):
        os.makedirs(os.path.dirname(cls.FILE_PATH), exist_ok=True)
        with open(cls.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def load(cls) -> dict:
        if not os.path.exists(cls.FILE_PATH):
            return {}
        with open(cls.FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
