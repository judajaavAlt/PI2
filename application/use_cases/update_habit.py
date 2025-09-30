from domain.entities.habit import Habit
from domain.value_objects.name import Name
from domain.value_objects.streak import Streak
from domain.value_objects.frequency import Frequency
from domain.value_objects.description import Description
from domain.repositories.habit_repository import HabitRepository


class UpdateHabit:
    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def execute(self, id: int, name: str, description: str,
                frequency: list, is_completed: bool, streak: int):
        habit = Habit(Name(name),
                      Description(description),
                      frequency=Frequency(frequency),
                      is_completed=is_completed,
                      streak=Streak(streak))
        return self.repository.update_habit(id, habit)
