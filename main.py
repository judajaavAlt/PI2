from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository
from infraestructure.ui.ui import UiStarter
from application.controllers.update_controller import UpdateController

uses = HabitSqliteRepository()
UpdateController.start()
UiStarter.start()
