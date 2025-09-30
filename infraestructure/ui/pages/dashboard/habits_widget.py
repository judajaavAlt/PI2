from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QCheckBox
from application.use_cases.list_habits import ListHabits
from application.use_cases.update_habit import UpdateHabit
from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository
from application.controllers.habit_controller import HabitController


class HabitsWidget(QWidget):
    """
    Widget que muestra directamente la lista de hábitos del día en un scroll.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = HabitController()

        # Repositorio y casos de uso
        self.repo = HabitSqliteRepository()
        self.list_habits_uc = ListHabits(self.repo)
        self.update_habit_uc = UpdateHabit(self.repo)

        # Layout principal
        main_layout = QVBoxLayout(self)
        self.setStyleSheet("""
            QCheckBox {
                color: black;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #0078d7;
                border-radius: 3px;
                background: white;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d7;
                border: 2px solid #0078d7;
            }
        """)

        # Scroll con contenido
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)

        self.scroll_content.setMinimumHeight(200)

        main_layout.addWidget(self.scroll)

        # Cargar hábitos
        self.load_habits()

    def load_habits(self):
        # Eliminar todos los widgets del layout (si hay alguno)
        for i in range(self.scroll_layout.count()):
            widget_item = self.scroll_layout.itemAt(i)
            if widget_item.widget():
                widget_item.widget().deleteLater()

        """Carga y muestra los hábitos del día."""
        habits = self.list_habits_uc.execute()

        if not habits:
            self.scroll_layout.addWidget(QLabel("⚠️ No hay hábitos para hoy."))
            return

        for habit in habits:
            # Filtrar solo los del día
            if habit.frequency.is_today():
                checkbox = QCheckBox(habit.name.value)
                checkbox.setChecked(habit.is_completed)
                checkbox.stateChanged.connect(
                    lambda state, h=habit:
                    self.change_habit_state(h))
                self.scroll_layout.addWidget(checkbox)

        self.scroll_layout.addStretch()

        self.scroll_content.updateGeometry()
        self.scroll.update()
        self.scroll.ensureWidgetVisible(self.scroll_content)

    def change_habit_state(self, habit):
        habit_changed = self.controller.switch_habit_state(habit)
        self.controller.update_habit(habit_changed)
        self.parent.update_widgets()

    def update_habit(self, habit):
        """Actualiza el hábito cuando se cambia el estado."""
        self.update_habit_uc.execute(
            habit.habit_id,
            habit.name.value,
            habit.description.value,
            habit.frequency.value,
            habit.is_completed,
            habit.streak.value
        )
