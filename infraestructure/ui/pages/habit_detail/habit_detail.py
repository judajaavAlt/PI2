from PySide6.QtWidgets import QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path


class HabitDetailPage:
    def __init__(self):
        self.load_ui_file()

    def load_ui_file(self):
        loader = QUiLoader()
        page_ui_path = generate_ui_file_path("habit_detail_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()

    def set_props(self, props: dict):
        self.show_detail_view(props)

    # Views logic
    def show_detail_view(self, props: dict):
        # Set habit props in detail fields
        label_habit_name = self.window.findChild(QLabel, "label_habit_name")
        label_habit_name.setText(props["name"])

        label_habit_desc = self.window.findChild(QLabel, "label_habit_desc")
        label_habit_desc.setText(props["description"])
        label_habit_desc.setWordWrap(True)

        label_habit_freq = self.window.findChild(QLabel, "label_habit_freq")
        label_habit_freq.setText(props["description"])

        print("Props recibidos en HabitDetailPage:", props)
