from infraestructure.persistence.paths import paths


class Profile:
    def __init__(self, name: str = ""):
        self.name = name
        self.photo_path = paths.get_pfp_path()

    def to_dict(self):
        return {"name": self.name, "photo": self.photo_path}

    @staticmethod
    def from_dict(d: dict):
        return Profile(name=d.get("name", ""))
