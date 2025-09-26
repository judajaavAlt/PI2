import sqlite3
from domain.repositories.habit_repository import HabitRepository
from infraestructure.persistence.paths import paths


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
                    status TEXT NOT NULL CHECK(status IN ('completed', 'missed')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
                );
                """
            )

            conn.commit()
            print("📦 Tablas creadas (si no existían)")


    def create_habit(self):
        pass