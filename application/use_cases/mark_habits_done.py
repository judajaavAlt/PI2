from domain.entities.habit import Habit
from domain.repositories.habit_repository import HabitRepository


class SwitchHabitState:
    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def execute(self, id: int, habit: Habit):
        new_habit = habit.copy()
        new_habit.is_completed = not habit.is_completed
        return self.repository.update_habit(id, habit)
