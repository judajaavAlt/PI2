
from abc import ABC, abstractmethod
from domain.entities.profile import Profile

class UserRepository(ABC):
    @abstractmethod
    def save_user(self, profile: Profile) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_user(self) -> Profile:
        raise NotImplementedError
