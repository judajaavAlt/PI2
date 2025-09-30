from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os

from infraestructure.ui.pages.habits.habits_list import HabitsListWidget


def generate_ui_file_path(file: str):
    """Genera la ruta completa a un archivo .ui"""
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, file)


class HabitsPage:
    """
    Página de hábitos que carga su UI desde .ui y agrega el HabitsListWidget
    dentro del contenedor especificado.
    """

    def __init__(self, main_window=None):
        loader = QUiLoader()
        ui_path = generate_ui_file_path("habits_view.ui")
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No se pudo abrir el archivo UI en: {ui_path}")

        # Cargar UI
        self.window = loader.load(ui_file)
        ui_file.close()
        self.main_window = main_window

        # Encontrar el contenedor donde se insertará la lista
        container = self.window.findChild(QWidget, "habits_list_container")
        if container is None:
            raise RuntimeError(
                "No se encontró un contenedor "
                "llamado 'habits_list_container' en el .ui")

        # Crear layout si no existe
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout(container)

        # Agregar el widget de la lista de hábitos
        self.habits_list_widget = HabitsListWidget()
        layout.addWidget(self.habits_list_widget)

        # Conectar señal al método que abre la página de detalle
        self.habits_list_widget.habit_clicked.connect(self.open_habit_detail)

    def open_habit_detail(self, habit_dict):
        # Cambiar la vista a la página de detalle
        self.main_window.change_page(3, habit_dict)

    def uptate(self):
        self.habits_list_widget.update()
