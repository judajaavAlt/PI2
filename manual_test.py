from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository
from application.use_cases.list_habits import ListHabits
from application.use_cases.delete_habit import DeleteHabit
from domain.value_objects.name import Name
from domain.value_objects.description import Description
from domain.value_objects.frequency import Frequency
from domain.entities.habit import Habit
import sqlite3


def manual_test():
    repo = HabitSqliteRepository()

    # --- Paso 1: Insertamos hábitos quemados para probar ---
    conn = sqlite3.connect(repo.db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits")  # limpiamos
    cursor.execute("INSERT INTO habits (name, description, frequency) VALUES (?, ?, ?)",
                   ("Leer un libro", "Leer al menos 10 páginas", "daily"))
    cursor.execute("INSERT INTO habits (name, description, frequency) VALUES (?, ?, ?)",
                   ("Ir al gimnasio", "Hacer ejercicio 3 veces por semana", "weekly"))
    conn.commit()
    conn.close()

    # --- Paso 2: Listamos hábitos ---
    list_use_case = ListHabits(repo)
    habits = list_use_case.execute()
    print("📋 Lista de hábitos al inicio:")
    for h in habits:
        print("-", h)

    # --- Paso 3: Borramos un hábito ---
    habit_to_delete = habits[0]
    delete_use_case = DeleteHabit(repo)
    deleted = delete_use_case.execute(habit_to_delete.habit_id)
    print(f"\n🗑️ Borrando hábito: {deleted.name}")

    # --- Paso 4: Volvemos a listar ---
    habits = list_use_case.execute()
    print("\n📋 Lista de hábitos después de borrar:")
    for h in habits:
        print("-", h)


if __name__ == "__main__":
    manual_test()