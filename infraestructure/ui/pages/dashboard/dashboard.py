from PySide6.QtWidgets import QLabel, QProgressBar, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QFile
from application.controllers.habit_controller import HabitController
import os

from infraestructure.ui.pages.dashboard.habits_widget import HabitsWidget


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path


class DashboardPage (QWidget):
    def __init__(self):
        super().__init__()
        self.load_ui_file()
        self.controller = HabitController()
        self.setup_widgets()

    def load_ui_file(self):
        loader = QUiLoader()
        # page_ui_path = generate_ui_file_path("dashboard_view.ui")
        page_ui_path = generate_ui_file_path("dashboard_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()

    def set_progresses(self):
        habits_progress = self.controller.get_daily_progress_habits()
        print("progresos: ", habits_progress)
        todays_percentage = int(habits_progress["progress"])
        total_todays_habits = habits_progress["total"]
        completed_todays_habits = habits_progress["completed"]

        total_habits = 8  # habits_progress["total_habits"]
        total_streak_habits = 3  # habits_progress["total_streak"]
        streak_percentage = 0.8  # habits_progress["progress_streak"]

        # Set labels text
        label_banner_text: QLabel = self.window.findChild(
            QLabel, "bannerSubtext")
        today_progress_text: QLabel = self.window.findChild(
            QLabel, "todayProgressText")
        streak_progress_text: QLabel = self.window.findChild(
            QLabel, "streakProgressText")
        label_banner_text.setText(
            f'Has completado {completed_todays_habits} '
            f'de {total_todays_habits} '
            'hábitos ¡Sigue así!'
        )
        today_progress_text.setText(
            f'{completed_todays_habits} de {total_todays_habits} completados')
        streak_progress_text.setText(
            f'{total_streak_habits} de {total_habits} con racha activa')

        # Set labels percentage
        label_main_percentage: QLabel = self.window.findChild(
            QLabel, "bannerPercentage")
        label_todays_percentage: QLabel = self.window.findChild(
            QLabel, "percentage")
        label_streak_percentage: QLabel = self.window.findChild(
            QLabel, "percentage_2"
        )
        label_main_percentage.setText(str(todays_percentage)+"%")
        label_todays_percentage.setText(str(todays_percentage)+"%")
        label_streak_percentage.setText(str(streak_percentage)+"%")

        # Set progress bars
        progress_bar_today: QProgressBar = self.window.findChild(
            QProgressBar, "progress_bar_today"
        )
        progress_bar_streak: QProgressBar = self.window.findChild(
            QProgressBar, "progress_bar_streak"
        )
        progress_bar_today.setValue(todays_percentage)
        progress_bar_streak.setValue(streak_percentage)

    def setup_widgets(self):
        self.set_progresses()
        # Crear el HabitsWidget
        self.habits_widget = HabitsWidget(self)

        # Asegurar tamaño mínimo del widget
        self.habits_widget.setMinimumHeight(200)
        self.habits_widget.setMinimumWidth(200)

        # Crear layout vertical en el contenedor habitsContainer del UI
        self.habits_container_layout = QVBoxLayout(self.window.habitsContainer)
        self.habits_container_layout.addWidget(self.habits_widget)
        self.habits_container_layout.addStretch()

        # Forzar actualización del contenedor para que se muestre
        self.window.habitsContainer.updateGeometry()
        self.window.habitsContainer.repaint()

    def update_widgets(self):
        self.set_progresses()
        self.habits_widget.load_habits()
        self.window.habitsContainer.updateGeometry()
        self.window.habitsContainer.repaint()
