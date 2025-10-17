from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QCheckBox, QHBoxLayout)
from application.use_cases.list_habits import ListHabits
from application.use_cases.update_habit import UpdateHabit
from infraestructure.persistence.habit_repository_sqlite import (
    HabitSqliteRepository)
from application.controllers.habit_controller import HabitController


# Widget that shows a list of today's habits in a scroll area
class HabitsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = HabitController()

        # Repository and use cases
        self.repo = HabitSqliteRepository()
        self.list_habits_uc = ListHabits(self.repo)
        self.update_habit_uc = UpdateHabit(self.repo)

        # Create main layout
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

        # Create scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(150)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # Set space in scroll layout
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)

        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        # Load habits
        self.load_habits()

    def load_habits(self):
        # Delete any widget in layout
        for i in range(self.scroll_layout.count()):
            widget_item = self.scroll_layout.itemAt(i)
            if widget_item.widget():
                widget_item.widget().deleteLater()

        # Load today's habits
        habits = self.list_habits_uc.execute()

        if not habits:
            self.scroll_layout.addWidget(QLabel("⚠️ No hay hábitos para hoy."))
            return

        # Filter to get today's habits
        todays_habits = [h for h in habits if h.frequency.is_today()]

        # Sort habits so completed ones are firts, keeping a stable sort
        todays_habits = sorted(
            todays_habits,
            key=lambda h: h.is_completed,
            reverse=False
        )

        for habit in todays_habits:
            # Crear un contenedor horizontal
            container_layout = QHBoxLayout()

            # Create QCheckBox and QLabel
            checkbox = QCheckBox(habit.name.value)

            # checkbox.setMinimumHeight(20)
            checkbox.setChecked(habit.is_completed)
            checkbox.stateChanged.connect(
                lambda state, h=habit:
                self.change_habit_state(h))

            label = QLabel(f"{habit.streak} 🔥")

            # Add elements to layout
            container_layout.addWidget(checkbox)
            container_layout.addStretch()
            container_layout.addWidget(label)

            # Create a QWidget for layout and add it
            container_widget = QWidget()
            container_widget.setObjectName("habit_w")
            container_widget.setStyleSheet("""
                QWidget {
                    padding: 0;
                    border-radius: 3px;
                    max-height: 50px;
                }
                QWidget#habit_w:hover {
                    background-color: #DDDDDD;
                }
                QCheckBox {
                    background-color: transparent;
                }
                QLabel {
                    background-color: transparent;
                    font-weight: bold;
                }
            """)
            container_widget.setLayout(container_layout)

            self.scroll_layout.addWidget(container_widget)

        self.scroll_content.adjustSize()
        self.scroll_content.updateGeometry()
        self.scroll.ensureWidgetVisible(self.scroll_content)

    def change_habit_state(self, habit):
        self.controller.switch_habit_state(habit)
        self.parent.update_widgets()

    def open_habit_detail(self, habit_id):
        # Cambiar la vista a la página de detalle
        habit_dict = {"id": habit_id}
        self.parent.go_to_detail(habit_dict)

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
