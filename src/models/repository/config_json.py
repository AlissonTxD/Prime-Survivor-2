from typing import List
import json

PATH = "config.json"
BASE_CONFIG = {"hotkeys": {}, "logbot": {"token": "", "chat_id": "", "subimage_cut": [776, 213, 1146, 256], "whatapp": "abc123"}}

class ConfigRepository:
    def __init__(self) -> None:
        self.data = None
        self.__load_data(PATH)

    def __load_data(self, path: str) -> None:
        try:
            self.data = self.__open_json(path)
        except FileNotFoundError:
            with open(path, "w") as fp:
                json.dump(BASE_CONFIG, fp, indent=4)
            self.__load_data(path)

    def __open_json(self, path: str) -> list:
        with open(path, "r") as fp:
            var = json.load(fp)
            return var
        
    def save_config(self) -> None:
        with open(PATH, "w") as fp:
            json.dump(self.data, fp, indent=4)
        
        
if __name__ == "__main__":
    config = ConfigRepository()