from infraestructure.persistence.data_handler import DataHandler


class Preferences:
    @classmethod
    def save(cls, user_pref: dict):
        data = DataHandler.load_data()
        data["user_preferences"] = {"name": user_pref["name"]}
        DataHandler.save_data(data)

    @classmethod
    def load(cls) -> dict[str, str]:
        data = DataHandler.load_data()
        does_exists = "user_preferences" in data
        if not does_exists:
            print(data)
            data["user_preferences"] = {"name": "user"}
            print(data)
            DataHandler.save_data(data)
        return data["user_preferences"]
