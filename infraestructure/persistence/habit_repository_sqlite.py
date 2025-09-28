import sqlite3
from domain.repositories.habit_repository import HabitRepository
from infraestructure.persistence.paths import paths

# Value Objects
from domain.value_objects.name import Name
from domain.value_objects.description import Description
from domain.value_objects.frequency import Frequency
from domain.value_objects.streak import Streak

from domain.entities.habit import Habit
from application.dto.habit_dto import HabitDto
from domain.utils.checks import check_type


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
                    frequency TEXT NOT NULL, -- store list as JSON string
                    is_completed INTEGER NOT NULL DEFAULT 0, -- 0 or 1
                    streak INTEGER NOT NULL DEFAULT 0
                );
                """
            )

            conn.commit()
            print("Tablas creadas (si no existían)")

    def create_habit(self, habit: Habit) -> Habit:
        """Create a new habit in the database and return the created habit."""
        check_type("habit", habit, Habit)
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
            sql = """
            INSERT INTO habits (name, description, frequency,
                                is_completed, streak)
            VALUES (?, ?, ?, ?, ?)
            """
            values = HabitDto.domain_to_infraestructure(habit)[1:]
            cursor.execute(sql, values)
            conn.commit()
            habit_id = cursor.lastrowid
            new_habit = (habit_id,) + values
            return HabitDto.infraestructure_to_domain(new_habit)

    def update_habit(self, id: int, habit: Habit) -> Habit:
        """Update an existing habit in the database
        and return the updated habit."""
        check_type("habit", habit, Habit)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Check that the habit exists
            cursor.execute("SELECT habit_id FROM habits WHERE habit_id = ?",
                           (id,))
            existing_habit = cursor.fetchone()

            if not existing_habit:
                error_msg = f"Habit with id {id} does not exist."
                raise ValueError(error_msg)

            # Update habit in DB
            sql = """
            UPDATE habits
            SET name = ?, description = ?, frequency = ?, is_completed = ?,
                streak = ?
            WHERE habit_id = ?
            """
            values = HabitDto.domain_to_infraestructure(habit)[1:]
            cursor.execute(sql, values + (id,))
            conn.commit()

            # Build updated habit tuple
            updated_habit = (id,) + values
            return HabitDto.infraestructure_to_domain(updated_habit)

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
        return Habit(1, Name("a"), Description("A"))

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