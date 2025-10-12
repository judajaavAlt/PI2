from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository
from domain.entities.habit import Habit
from application.use_cases.create_habit import CreateHabit
from application.use_cases.mark_habits_done import SwitchHabitState
from application.use_cases.update_habit import UpdateHabit
from application.use_cases.delete_habit import DeleteHabit
from application.use_cases.list_habits import ListHabits
from application.use_cases.get_habit import GetHabit
from application.use_cases.habit_progress import HabitProgress
from application.use_cases.get_habit_name_existence import GetHabitNameExistence


class HabitController:
    repo = HabitSqliteRepository()

    @classmethod
    def create_habit(cls, name: str, description: str, frequency: list):
        return CreateHabit(cls.repo).execute(name, description, frequency)

    @classmethod
    def delete_habit(cls, habit_id: int):
        return DeleteHabit(cls.repo).execute(habit_id)
        pass

    @classmethod
    def get_habit(cls, habit_id: int):
        return GetHabit(cls.repo).execute(habit_id)
        pass

    @classmethod
    def list_habits(cls):
        return ListHabits(cls.repo).execute()
        pass

    @classmethod
    def switch_habit_state(cls, habit: Habit):
        return SwitchHabitState(cls.repo).execute(habit.habit_id, habit)

    @classmethod
    def update_habit(cls, habit: Habit):
        id = habit.habit_id
        name = habit.name.value
        description = habit.description.value
        frequency = habit.frequency.value
        is_completed = habit.is_completed
        streak = habit.streak.value
        return UpdateHabit(cls.repo).execute(
            id,
            name,
            description,
            frequency,
            is_completed,
            streak)

    @classmethod
    def get_daily_progress_habits(cls):
        return HabitProgress(cls.repo).execute()

    @classmethod
    def get_habit_name_existence(cls, name: str):
        return GetHabitNameExistence(cls.repo).execute(name)
