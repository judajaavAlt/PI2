from domain.entities.profile import Profile

class UpdateProfileUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, name: str, photo_path: str):
        profile = Profile(name=name, photo_path=photo_path)
        self.user_repository.save_user(profile)

    def load(self) -> Profile:
        return self.user_repository.load_user()
