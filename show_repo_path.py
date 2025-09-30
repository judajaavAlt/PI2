from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository
repo = HabitSqliteRepository()
print("DB path:", repo.db_path)