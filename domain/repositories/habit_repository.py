from abc import ABC, abstractmethod
from domain.entities.habit import Habit


class HabitRepository(ABC):
    @abstractmethod
    def create_habit(self, habit: Habit) -> Habit:
        pass

    @abstractmethod
    def update_habit(self, id: int, habit: Habit) -> Habit:
        pass

    @abstractmethod
    def delete_habit(self, id: int) -> Habit:
        pass

    @abstractmethod
    def get_habit(self, id: int) -> Habit:
        pass

    @abstractmethod
    def get_all_habits(self) -> list[Habit]:
        """Devuelve la lista de todos los habitos almacenados."""
        raise NotImplementedError