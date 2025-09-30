from PySide6.QtWidgets import QLabel, QProgressBar
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path


class DashboardPage:
    def __init__(self):
        self.load_ui_file()

        dummy_todays_percentage = 40
        dummy_streak_percentage = 80

        self.set_progresses(dummy_todays_percentage, dummy_streak_percentage)

    def set_progresses(self, todays_percentage: int, streak_percentage: int):
        # Set labels
        label_main_percentage: QLabel = self.window.findChild(
            QLabel, "bannerPercentage")
        label_todays_percentage: QLabel = self.window.findChild(
            QLabel, "percentage")
        label_streak_percentage: QLabel = self.window.findChild(
            QLabel, "percentage_2"
        )
        label_main_percentage.setText(str(todays_percentage))
        label_todays_percentage.setText(str(todays_percentage))
        label_streak_percentage.setText(str(streak_percentage))

        # Set progress bars
        progress_bar_today: QProgressBar = self.window.findChild(
            QProgressBar, "progress_bar_today"
        )
        progress_bar_streak: QProgressBar = self.window.findChild(
            QProgressBar, "progress_bar_streak"
        )
        progress_bar_today.setValue(todays_percentage)
        progress_bar_streak.setValue(streak_percentage)

    def load_ui_file(self):
        loader = QUiLoader()
        page_ui_path = generate_ui_file_path("dashboard_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()
