from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from application.controllers.habit_controller import HabitController
import os


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path


class HabitDetailPage:
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.props = None
        self.load_ui_file()
        self.controller = HabitController()

        # Get elements
        self.btn_edit: QPushButton = self.window.findChild(
            QPushButton, "btn_edit")
        self.btn_delete: QPushButton = self.window.findChild(
            QPushButton, "btn_delete")

        # Connect button
        self.btn_edit.clicked.connect(self.go_to_form)
        self.btn_delete.clicked.connect(self.delete_habit)

    def load_ui_file(self):
        loader = QUiLoader()
        page_ui_path = generate_ui_file_path("habit_detail_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()

    def set_props(self, props: dict):
        self.props = props
        id = props["id"]
        habit_props = self.controller.get_habit(id)
        self.show_detail_view(habit_props)

    # Views logic
    def show_detail_view(self, props):
        # Set habit props in detail fields
        label_habit_name = self.window.findChild(QLabel, "label_habit_name")
        label_habit_name.setText(str(props.name))

        label_habit_desc = self.window.findChild(QLabel, "label_habit_desc")
        label_habit_desc.setText(str(props.description))
        label_habit_desc.setWordWrap(True)

        label_habit_freq = self.window.findChild(QLabel, "label_habit_freq")
        habit_frequency = self.get_frequency_days(props.frequency)
        label_habit_freq.setText(habit_frequency)

    def get_frequency_days(self, days_array):
        week_days = [
            "Lunes", "Martes", "Miércoles", "Jueves",
            "Viernes", "Sábado", "Domingo"]
        active_days = [
            week_days[i] for i, active in enumerate(
                days_array.value) if active == 1]

        return ", ".join(active_days)

    def go_to_form(self):
        self.main_window.change_page(4, self.props)
        self.props = None

    def delete_habit(self):
        id = self.props["id"]
        self.controller.delete_habit(id)
        self.main_window.change_page(0)
        self.props = None
