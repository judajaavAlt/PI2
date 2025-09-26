from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path


class ConfigPage:
    def __init__(self):
        self.load_ui_file()

    def load_ui_file(self):
        loader = QUiLoader()
        page_ui_path = generate_ui_file_path("config_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()
