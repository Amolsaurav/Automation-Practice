import json
import os

class DataLoader:

    @staticmethod
    def load_json(file_name):
        data_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "TestData")
        file_path = os.path.join(data_directory, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)