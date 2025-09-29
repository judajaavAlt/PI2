from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository
from infraestructure.ui.ui import UiStarter


uses = HabitSqliteRepository()
UiStarter.start()
