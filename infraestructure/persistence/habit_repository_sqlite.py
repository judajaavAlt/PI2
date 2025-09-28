import sqlite3
from domain.repositories.habit_repository import HabitRepository
from infraestructure.persistence.paths import paths

# Value Objects
from domain.value_objects.name import Name
from domain.value_objects.description import Description
from domain.value_objects.frequency import Frequency
from domain.value_objects.streak import Streak

from domain.entities.habit import Habit


class HabitSqliteRepository(HabitRepository):

    def __init__(self):
        """Inicializa el repositorio y asegura que las tablas existan."""
        self.db_path = paths.get_db_path()
        self._create_tables()

    def _create_tables(self):
        """Crea las tablas necesarias si no existen."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    frequency TEXT NOT NULL, -- Ej: 'daily', 'weekly', 'custom'
                    is_active INTEGER DEFAULT 1, -- 1 = activo, 0 = eliminado
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS habit_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('completed',
                    'missed')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON
                    DELETE CASCADE
                );
                """
            )

            conn.commit()
            print("📦 Tablas creadas (si no existían)")

    def create_habit(self, habit: Habit) -> Habit:
        """Create a new habit in the database and return the created habit."""
        # Early stop if habit already exists
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT habit_id FROM habits WHERE habit_id = ?",
                           (habit.habit_id,))
            existing_habit = cursor.fetchone()

            if existing_habit:
                error_msg = f"Habit with id {habit.habit_id} already exists."
                raise ValueError(error_msg)

            # Insert new habit into the database
            insert_sql = """
            INSERT INTO habits (habit_id, name, description, frequency,
            streak, is_completed)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_sql, (
                habit.habit_id,
                habit.name,
                habit.description,
                habit.frequency.value if habit.frequency else None,
                habit.streak.value if habit.streak else 0,
                habit.is_completed
            ))
            conn.commit()

        return habit

    def update_habit(self, id: int, habit: Habit) -> Habit:
        pass

    def delete_habit(self, id: int) -> Habit:
        """Elimina un hábito por su id y devuelve el hábito eliminado."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Buscar primero el hábito
            cursor.execute("SELECT habit_id, name, description, frequency, is_active FROM habits WHERE habit_id = ?", (id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Habit with id {id} not found")

            # Construimos el objeto Habit ANTES de borrarlo
            habit = Habit(
                habit_id=row[0],
                name=Name(row[1]),
                description=Description(row[2]),
                frequency=Frequency,
                streak=Streak(0)  # lo inicializamos en 0 por ahora
            )

            # Borrar (aquí lo elimino físicamente, podrías cambiarlo por UPDATE is_active=0)
            cursor.execute("DELETE FROM habits WHERE habit_id = ?", (id,))
            conn.commit()

            return habit

    def get_habit(self, id: int) -> Habit:
        pass

    def get_all_habits(self) -> list[Habit]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT habit_id, name, description, frequency, is_active
                FROM habits
                WHERE is_active = 1
            """)
            rows = cursor.fetchall()

            habits = []
            for row in rows:
                freq_text = row[3]

                # Construcción del VO Frequency según lo que venga en DB
                frequency = Frequency()
                if freq_text == "daily":
                    # Activamos todos los días
                    for day in Frequency.DAYS:
                        frequency.set_day(day)
                elif freq_text == "weekly":
                    # Activamos solo lunes como ejemplo
                    frequency.set_day("lunes")
                else:
                    # Si no es un valor reconocido, lo dejamos vacío
                    frequency = Frequency()

                habit = Habit(
                    habit_id=row[0],
                    name=Name(row[1]),
                    description=Description(row[2]),
                    frequency=frequency,
                    streak=Streak(0)  # por ahora arrancamos en 0
                )
                habits.append(habit)

            return habits