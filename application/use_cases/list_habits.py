from domain.repositories.habit_repository import HabitRepository


class ListHabits:
    def __init__(self, habit_repository: HabitRepository):
        self.habit_repository = habit_repository

    def execute(self):
        """Devuelve todos los hábitos activos."""
        return self.habit_repository.get_all_habits()