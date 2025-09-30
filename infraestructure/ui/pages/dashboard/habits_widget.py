from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QScrollArea
from application.use_cases.list_habits import ListHabits
from application.use_cases.mark_habits_done import SwitchHabitState
from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository

class HabitsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal con scroll
        layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.scroll_area.setWidget(self.content)

        layout.addWidget(self.scroll_area)

        # Repositorio y casos de uso
        self.repo = HabitSqliteRepository()
        self.list_habits_uc = ListHabits(self.repo)
        self.switch_habit_uc = SwitchHabitState(self.repo)

        # Cargar hábitos
        self.load_habits()

    def load_habits(self):
        # Limpiar contenido anterior
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Obtener hábitos
        habits = self.list_habits_uc.execute()
        print(f"Habits loaded: {habits}")  # Para debug

        # Ordenar: completados primero
        habits_sorted = sorted(habits, key=lambda h: not h.is_completed)

        # Renderizar cada hábito
        for habit in habits_sorted:
            row = QWidget()
            row_layout = QHBoxLayout(row)

            # Checkbox a la izquierda
            checkbox = QCheckBox()
            checkbox.setChecked(habit.is_completed)
            checkbox.stateChanged.connect(lambda state, h=habit: self.switch_habit_uc.execute(h, state))
            row_layout.addWidget(checkbox)

            # Texto del hábito a la derecha
            label = QLabel(habit.name.value)  # <-- Asegúrate de usar .value
            row_layout.addWidget(label)

            self.content_layout.addWidget(row)

        # Empujar elementos hacia arriba
        self.content_layout.addStretch()
