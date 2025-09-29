from domain.repositories.user_repository import UserRepository
from domain.entities.profile import Profile
from settings.preferences import Preferences

class PreferencesUserRepository(UserRepository):
    def save_user(self, profile: Profile) -> None:
        Preferences.save(profile.to_dict())

    def load_user(self) -> Profile:
        data = Preferences.load()
        return Profile.from_dict(data)
