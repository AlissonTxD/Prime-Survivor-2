from typing import List
import json

PATH = "config.json"


class ConfigRepository:
    def __init__(self) -> None:
        self.data = None
        self.__load_data(PATH)

    def get_json_data(self, path: str= PATH) -> List:
        self.__load_data(path)
        return self.data
    
    def save_json(self, obj: List, path: str) -> None:
        with open(path, "w") as fp:
            json.dump(obj, fp, indent=2)

    def __load_data(self, path: str) -> None:
        try:
            self.data = self.__open_json(path)
        except FileNotFoundError:
            with open(path, "w") as fp:
                json.dump([], fp)

    def __open_json(self, path: str) -> list:
        with open(path, "r") as fp:
            var = json.load(fp)
            return var
        
        
if __name__ == "__main__":
    config = ConfigRepository()
    print(config.data)