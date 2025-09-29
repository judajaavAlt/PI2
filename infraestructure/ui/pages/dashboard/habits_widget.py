from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QCheckBox, QLabel
from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository
from application.use_cases.list_habits import ListHabits
from application.use_cases.mark_habits_done import SwitchHabitState

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
        print("Habits loaded:", habits)  # Para debug

        # Ordenar: completados primero
        habits_sorted = sorted(habits, key=lambda h: not h.is_completed)

        # Crear filas: checkbox a la izquierda, texto a la derecha
        for habit in habits_sorted:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            
            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(habit.is_completed)
            checkbox.stateChanged.connect(lambda state, h=habit: self.switch_habit_uc.execute(h, state))
            row_layout.addWidget(checkbox)
            
            # Texto del hábito
            label = QLabel(habit.name)
            row_layout.addWidget(label)

            # Alineación y estiramiento
            row_layout.addStretch()
            
            # Añadir fila al layout principal
            self.content_layout.addWidget(row_widget)

        # Empujar todo hacia arriba
        self.content_layout.addStretch()
