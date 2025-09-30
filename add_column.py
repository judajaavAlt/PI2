import sqlite3
from infraestructure.persistence.paths import paths
import json

db_path = paths.get_db_path()

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Borrar todos los hábitos existentes
    cursor.execute("DELETE FROM habits;")
    conn.commit()

    # Insertar nuevos hábitos con 7 días (0 = no, 1 = sí)
    habits_to_insert = [
        ("Leer 30 min", "Leer libros o artículos", json.dumps([1,1,1,1,1,1,1]), 0, 0),
        ("Hacer ejercicio", "Ejercicios de fuerza y cardio", json.dumps([1,0,1,0,1,0,0]), 0, 0),
        ("Meditar", "Meditar 10 minutos", json.dumps([0,1,0,1,0,1,0]), 0, 0),
    ]

    cursor.executemany(
        "INSERT INTO habits (name, description, frequency, is_completed, streak) VALUES (?, ?, ?, ?, ?);",
        habits_to_insert
    )
    conn.commit()

    print("Hábito(s) creado(s) correctamente con 7 días en frequency.")
