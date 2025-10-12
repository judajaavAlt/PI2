from domain.repositories.habit_repository import HabitRepository


class GetHabitNameExistence:
    def __init__(self, habit_repository: HabitRepository):
        self.habit_repository = habit_repository

    def execute(self, name: str):
        """ Retorna True si ya existe un hábito con ese nombre, si no False """

        habits = self.habit_repository.get_all_habits()
        for habit in habits:
            if habit.name.value.lower() == name.lower():
                return True

        return False
