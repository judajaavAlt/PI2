from PySide6.QtWidgets import QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path


class HabitFormPage:
    def __init__(self):
        self.load_ui_file()

    def load_ui_file(self):
        loader = QUiLoader()
        page_ui_path = generate_ui_file_path("habit_form_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()

    def set_props(self, props: dict | None):
        if props:
            self.show_edit_view(props)
        else:
            self.show_create_view()

    # Views logic
    def show_edit_view(self, props: dict):
        # Set habit props in fields
        # label_habit_name = self.window.findChild(QLabel, "label_habit_name")
        # label_habit_name.setText(props["name"])

        # label_habit_desc = self.window.findChild(QLabel, "label_habit_desc")
        # label_habit_desc.setText(props["description"])
        # label_habit_desc.setWordWrap(True)

        # label_habit_freq = self.window.findChild(QLabel, "label_habit_freq")
        # label_habit_freq.setText(props["description"])

        print("Props recibidos en HabitModulePage:", props)

    def show_create_view(self):
        # Si tienes campos QLineEdit para editar:
        # - Si entras desde editar → llenas con props
        # - Si es nuevo → los dejas vacíos
        # Ejemplo:
        # txt_name = self.window.findChild(QLineEdit, "txt_habit_name")
        # if txt_name:
        #     txt_name.setText(self.current_props["habit_name"] if
        # hasattr(self, "current_props") else "")
        pass
