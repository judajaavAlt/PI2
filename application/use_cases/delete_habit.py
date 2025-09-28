from domain.repositories.habit_repository import HabitRepository


class DeleteHabit:
    def __init__(self, habit_repository: HabitRepository):
        self.habit_repository = habit_repository

    def execute(self, habit_id: int):
        """Elimina un hábito por id y devuelve el hábito eliminado."""
        return self.habit_repository.delete_habit(habit_id)