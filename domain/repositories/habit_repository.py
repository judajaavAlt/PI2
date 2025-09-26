from abc import ABC, abstractmethod


class HabitRepository(ABC):
    @abstractmethod
    def create_habit(self):
        pass
