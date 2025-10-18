from domain.entities.profile import Profile
from infraestructure.persistence.file_manager import FileManager
from infraestructure.persistence.paths import paths


class UpdateProfileUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, name: str, photo_path: str):
        profile = Profile(name=name)
        FileManager.convert_to_webp(photo_path, paths.get_pfp_path())
        FileManager.clip_to_square(paths.get_pfp_path(), paths.get_pfp_path())
        self.user_repository.save_user(profile)

    def load(self) -> Profile:
        return self.user_repository.load_user()
