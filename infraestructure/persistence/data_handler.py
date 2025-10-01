from infraestructure.persistence.paths import paths
import json


class DataHandler:
    path = paths.get_data_path()

    @classmethod
    def save_data(cls, content) -> None:
        with open(cls.path, "wt") as file:
            file.write(json.dumps(content))

    @classmethod
    def load_data(cls) -> dict:
        try:
            with open(cls.path, "rt") as file:
                content = json.loads(file.read())
            return content

        except FileNotFoundError:
            with open(cls.path, "wt") as file:
                file.write(json.dumps({}))
            return {}
