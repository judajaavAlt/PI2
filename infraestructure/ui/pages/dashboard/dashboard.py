from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QFile
import os

from infraestructure.ui.pages.dashboard.habits_widget import HabitsWidget

def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path

class DashboardPage:
    def __init__(self):
        self.load_ui_file()
        self.setup_widgets()  

    def load_ui_file(self):
        loader = QUiLoader()
        page_ui_path = generate_ui_file_path("dashboard_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()
    
    def setup_widgets(self):
        # Crear el HabitsWidget
        self.habits_widget = HabitsWidget()
        
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
