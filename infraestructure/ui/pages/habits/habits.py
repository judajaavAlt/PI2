from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtGui import QColor, QPalette

# Repositorio y casos de uso (igual que tu ejemplo)
from application.use_cases.list_habits import ListHabits
from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository


class HabitItemWidget(QWidget):
    """
    Widget que representa un hábito en la lista, con nombre, id y color.
    """
    def __init__(self, habit, parent=None):
        super().__init__(parent)
        self.habit = habit

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Color identificador
        color_label = QLabel()
        color_label.setFixedSize(20, 20)
        color_label.setStyleSheet(f"background-color: {habit.color}; border-radius: 10px;")
        layout.addWidget(color_label)

        # Nombre del hábito
        name_label = QLabel(f"{habit.name.value} (ID: {habit.habit_id})")
        layout.addWidget(name_label)

        layout.addStretch()


class HabitsListWidget(QWidget):
    """
    Widget que muestra la lista de hábitos en un QListWidget.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.repo = HabitSqliteRepository()
        self.list_habits_uc = ListHabits(self.repo)

        main_layout = QVBoxLayout(self)

        # Lista de hábitos
        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)

        self.load_habits()

    def load_habits(self):
        """Carga y muestra todos los hábitos."""
        habits = self.list_habits_uc.execute()

        if not habits:
            self.list_widget.addItem("⚠️ No hay hábitos registrados.")
            return

        for habit in habits:
            item_widget = HabitItemWidget(habit)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())

            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)

