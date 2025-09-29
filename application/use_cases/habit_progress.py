from domain.repositories.habit_repository import HabitRepository
from datetime import datetime


class HabitProgress:
    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def daily_progress(self) -> float:
        """
        Calcula el progreso diario en porcentaje.
        - Se toman todos los hábitos que corresponden al día actual.
        - Se calcula el porcentaje de los que han sido completados.
        Devuelve un valor entre 0.0 y 100.0
        """

        today = datetime.now().strftime("%A").lower()  # ejemplo: "monday"
        habits = self.repository.get_all_habits()

        # Filtrar los hábitos que aplican para el día de hoy
        today_habits = [h for h in habits if today in h.frequency.value]

        if not today_habits:  # Si no hay hábitos para hoy, el progreso es 0
            return 0.0

        completed = sum(1 for h in today_habits if h.is_completed)
        progress = (completed / len(today_habits)) * 100

        return round(progress, 2)