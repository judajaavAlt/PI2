from infraestructure.persistence.data_handler import DataHandler
from infraestructure.persistence.time import TimeManager as tm
from application.use_cases.update_streak import UpdateStreak
from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository
from application.controllers.habit_controller import HabitController


class UpdateController:
    @classmethod
    def start(cls):
        # gets last date
        data = DataHandler.load_data()
        key_doesnt_exist = "last_date" not in data.keys()
        last_date = tm.now() if key_doesnt_exist else data["last_date"]
        data["last_date"] = last_date
        DataHandler.save_data(data)

        # updates streak and state
        habits = HabitController.list_habits()
        time_distance = tm.days_distance(last_date, tm.now())
        if time_distance >= 1:
            fun = UpdateStreak(HabitSqliteRepository())
            for habit in habits:
                fun.execute(habit)

        # Saves the new last date
        data["last_date"] = tm.now()
        DataHandler.save_data(data)
