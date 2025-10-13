from domain.entities.habit import Habit
from domain.repositories.habit_repository import HabitRepository
from infraestructure.persistence.time import TimeManager as tm


class UpdateStreak:
    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def execute(self, habit: Habit, days_passed):
        lost_days = tm.get_lost_days(days_passed)
        habit_days = habit.frequency.value
        keep_streak = sum([lost_days[i] & habit_days[i] for i in range(7)]) == 0
        
        if keep_streak:
            habit.modify(streak=habit.streak.increase().value)
        else:
            habit.modify(streak=habit.streak.reset().value)

        habit.modify(is_completed=False)

        return self.repository.update_habit(habit.habit_id, habit)
