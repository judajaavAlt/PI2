from domain.entities.habit import Habit
from domain.repositories.habit_repository import HabitRepository


class UpdateStreak:
    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def execute(self, habit: Habit, keep_streak: bool):
        if keep_streak:
            habit.modify(streak=habit.streak.increase().value)
        else:
            habit.modify(streak=habit.streak.reset())

        habit.modify(is_completed=False)

        return self.repository.update_habit(habit.habit_id, habit)
