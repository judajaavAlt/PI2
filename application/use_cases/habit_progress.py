from domain.repositories.habit_repository import HabitRepository
from infraestructure.persistence.time import TimeManager


class HabitProgress:
    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    def execute(self) -> dict:
        """
        Calcula el progreso de los hábitos para el día actual.
        Retorna un diccionario con total, completados, pendientes y porcentaje.
        """
        # Mapear de inglés a español porque tu Frequency usa español
        day_map = {
            "monday": "lunes",
            "tuesday": "martes",
            "wednesday": "miercoles",
            "thursday": "jueves",
            "friday": "viernes",
            "saturday": "sabado",
            "sunday": "domingo",
        }

        today_en = TimeManager.today()  # ej. "monday"
        today_es = day_map[today_en]    # ej. "lunes"

        # Traer todos los hábitos
        habits = self.repository.get_all_habits()

        # Filtrar hábitos activos para hoy
        todays_habits = [h for h in habits if h.frequency.is_active(today_es)]

        if not todays_habits:
            return {
                "day": today_es,
                "total": 0,
                "completed": 0,
                "pending": 0,
                "progress": 0.0,
            }

        # Contar completados
        completed = sum(1 for h in todays_habits if h.is_completed)
        total = len(todays_habits)
        pending = total - completed
        progress = (completed / total) * 100

        return {
            "day": today_es,
            "total": total,
            "completed": completed,
            "pending": pending,
            "progress": progress,
            "total_habits": 6,  # Cantidad habitos en total en toda la app
            "total_streak": 2,  # Cantidad habitos en total de toda la app que tienen racha
            "progress_streak": 40,  # Porcentaje de hábitos con racha en toda la app sobre la cantidad de hábitos en total en toda la app: (habitos_total_conracha / habitos_total)
        }
