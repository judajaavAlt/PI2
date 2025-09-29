from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QCheckBox

class HabitWidget(QWidget):
    def __init__(self, habit, switch_habit_uc):
        super().__init__()

        # Layout vertical para cada hábito
        layout = QVBoxLayout(self)

        # Nombre del hábito
        self.name_label = QLabel(habit.name)
        layout.addWidget(self.name_label)

        # Descripción (opcional)
        if hasattr(habit, 'description'):
            self.description_label = QLabel(habit.description)
            layout.addWidget(self.description_label)

        # Checkbox para completado
        self.checkbox = QCheckBox("Completado")
        self.checkbox.setChecked(habit.is_completed)
        layout.addWidget(self.checkbox)

        # Conectar acción al caso de uso
        self.checkbox.stateChanged.connect(lambda state: switch_habit_uc.execute(habit, state))
