import json
import os


class DataLoader:

    @staticmethod
    def load_json(file_name):
        project_directory = os.path.dirname(os.path.dirname(__file__))
        DataLoader._load_env_file(os.path.join(project_directory, ".env"))

        data_directory = os.path.join(project_directory, "TestData")
        file_path = os.path.join(data_directory, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for records in data.values():
            if not isinstance(records, list):
                continue
            for record in records:
                record_id = record.get("id")
                password_key = f"TEST_PASSWORD_{record_id}"
                if "password" not in record and password_key in os.environ:
                    record["password"] = os.environ[password_key]

        return data

    @staticmethod
    def _load_env_file(file_path):
        if not os.path.exists(file_path):
            return

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))