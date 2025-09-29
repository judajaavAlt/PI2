from domain.entities.habit import Habit
from domain.value_objects.name import Name
from domain.value_objects.frequency import Frequency
from domain.value_objects.description import Description
from domain.repositories.habit_repository import HabitRepository


class CreateHabit:
    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def execute(self, name: str, description: str, frequency: Frequency):
        habit = Habit(Name(name),
                      Description(description),
                      frequency=Frequency(frequency))
        return self.repository.create_habit(habit)
