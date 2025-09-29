from domain.repositories.habit_repository import HabitRepository


class GetHabit:
    def __init__(self, habit_repository: HabitRepository):
        self.habit_repository = habit_repository

    def execute(self, habit_id: int):
        """Devuelve un hábito por id o None si no existe."""
        return self.habit_repository.get_habit(habit_id)