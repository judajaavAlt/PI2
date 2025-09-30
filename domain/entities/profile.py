class Profile:
    def __init__(self, name: str = "", photo_path: str = ""):
        self.name = name
        self.photo_path = photo_path

    def to_dict(self):
        return {"name": self.name, "photo": self.photo_path}

    @staticmethod
    def from_dict(d: dict):
        return Profile(name=d.get("name", ""), photo_path=d.get("photo", ""))
