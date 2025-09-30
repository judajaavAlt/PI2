import sqlite3
from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository

repo = HabitSqliteRepository()
db = repo.db_path

conn = sqlite3.connect(db)
cursor = conn.cursor()
print("TABLE habits rows:")
for row in cursor.execute("SELECT habit_id, name, description, frequency, is_active FROM habits"):
    print(row)
for col in cursor.execute("PRAGMA table_info(habits)"):
    print(col)
conn.close()