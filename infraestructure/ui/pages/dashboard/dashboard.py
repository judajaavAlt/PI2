from PySide6.QtWidgets import QLabel, QProgressBar, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QFile
from application.controllers.habit_controller import HabitController
import os

from infraestructure.ui.pages.dashboard.habits_widget import HabitsWidget
from application.use_cases.update_profile_use_case import UpdateProfileUseCase
from infraestructure.repositories.preferences_user_repository import PreferencesUserRepository


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, file)


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.load_ui_file()
        self.controller = HabitController()
        # Agregar el use case para cargar el perfil del usuario
        self.profile_use_case = UpdateProfileUseCase(
            PreferencesUserRepository())
        self.setup_widgets()

    def load_ui_file(self):
        loader = QUiLoader()
        page_ui_path = generate_ui_file_path("dashboard_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()

    def get_user_name(self):
        """Obtiene el nombre del usuario desde el perfil guardado"""
        profile = self.profile_use_case.load()
        if profile and profile.name:
            return profile.name
        return "Usuario"  # Nombre por defecto si no hay perfil guardado

    def set_progresses(self):
        habits_progress = self.controller.get_daily_progress_habits()
        todays_percentage = int(habits_progress["progress"])
        total_todays_habits = habits_progress["total"]
        completed_todays_habits = habits_progress["completed"]

        total_habits = habits_progress["total_habits"]
        total_streak_habits = habits_progress["total_streak"]
        streak_percentage = habits_progress["progress_streak"]

        # Obtener el nombre del usuario
        user_name = self.get_user_name()

        # Set labels text
        label_banner_text: QLabel = self.window.findChild(
            QLabel, "bannerSubtext")
        today_progress_text: QLabel = self.window.findChild(
            QLabel, "todayProgressText")
        streak_progress_text: QLabel = self.window.findChild(
            QLabel, "streakProgressText")

        # Actualizar el saludo con el nombre del usuario
        banner_greeting: QLabel = self.window.findChild(
            QLabel, "bannerGreeting")
        if banner_greeting:
            banner_greeting.setText(
                f"Increíble progreso el día de hoy {user_name}!")

        if label_banner_text:
            label_banner_text.setText(
                f'Has completado {completed_todays_habits} '
                f'de {total_todays_habits} '
                'hábitos ¡Sigue así!'
            )
        if today_progress_text:
            today_progress_text.setText(
                f'{completed_todays_habits} de {total_todays_habits} '
                'completados')
        if streak_progress_text:
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
        progress_bar_streak.setValue(streak_percentage*100)

    def setup_widgets(self):
        # Crear layout vertical en el contenedor habitsContainer del UI
        self.habits_container_layout = QVBoxLayout(self.window.habitsContainer)
        # self.habits_container_layout.addWidget(self.habits_widget)
        self.habits_container_layout.addStretch()

        self.update_habit_widget()

    def update_habit_widget(self):
        self.set_progresses()

        # Eliminar todos los widgets del layout (si hay alguno)
        for i in range(self.habits_container_layout.count()):
            widget_item = self.habits_container_layout.itemAt(i)
            if widget_item.widget():
                widget_item.widget().deleteLater()

        # Crear el HabitsWidget
        self.habits_widget = HabitsWidget(self)

        # Asegurar tamaño del widget
        self.habits_widget.setFixedHeight(170)

        self.habits_container_layout.addWidget(self.habits_widget)

        # Forzar actualización del contenedor para que se muestre
        self.window.habitsContainer.updateGeometry()
        self.window.habitsContainer.repaint()

    def update_widgets(self):
        self.habits_widget.load_habits()
        self.update_habit_widget()
