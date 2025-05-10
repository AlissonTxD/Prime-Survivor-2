from typing import List
import json

PATH = "config.json"
BASE_CONFIG = {
    "hotkeys": {
        "lineedit_input_logbot_start": "F8",
        "lineedit_input_stop": "F10",
        "lineedit_input_autoclick": "F9",
        "lineedit_input_toggleaim": "F2"
    },
    "logbot": {
        "token": "discord token",
        "channel_id": "channel id discord",
        "subimage_cut": [776, 213, 1146, 256],
        "whatsapp": "none",
    },
}


class ConfigRepository:
    def __init__(self) -> None:
        self.data = {}
        self.load_data(PATH)

    def load_data(self, path: str) -> None:
        try:
            self.data = self.__open_json(path)
        except FileNotFoundError:
            with open(path, "w") as fp:
                json.dump(BASE_CONFIG, fp, indent=4)
            self.load_data(path)

    def __open_json(self, path: str) -> list:
        with open(path, "r") as fp:
            var = json.load(fp)
            return var

    def save_config(self) -> None:
        with open(PATH, "w") as fp:
            json.dump(self.data, fp, indent=4)

    def reload_config(self) -> None:
        self.data = self.__open_json(PATH)


if __name__ == "__main__":
    config = ConfigRepository()
    print(config.data["hotkeys"])
