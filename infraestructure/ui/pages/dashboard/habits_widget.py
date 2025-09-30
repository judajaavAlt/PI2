from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QCheckBox
from application.use_cases.list_habits import ListHabits
from application.use_cases.update_habit import UpdateHabit
from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository


class HabitsWidget(QWidget):
    """
    Widget que muestra directamente la lista de hábitos del día en un scroll.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Repositorio y casos de uso
        self.repo = HabitSqliteRepository()
        self.list_habits_uc = ListHabits(self.repo)
        self.update_habit_uc = UpdateHabit(self.repo)

        # Layout principal
        main_layout = QVBoxLayout(self)

        # Scroll con contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Cargar hábitos
        self.load_habits()

    def load_habits(self):
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
                checkbox.stateChanged.connect(lambda state, h=habit: self.update_habit(h))
                self.scroll_layout.addWidget(checkbox)

        self.scroll_layout.addStretch()

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

