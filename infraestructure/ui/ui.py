from PySide6.QtWidgets import QApplication, QPushButton, QStackedWidget, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os
from infraestructure.ui.pages.config.config import ConfigPage
from infraestructure.ui.pages.dashboard.dashboard import DashboardPage
from infraestructure.ui.pages.habits.habits import HabitsPage


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path


# Window class
class MainWindow:
    def __init__(self):
        self.load_ui_file()

        # Access the widgets by their objectName
        self.btn_sidebar_1: QPushButton = self.window.findChild(
            QPushButton, "btn_sidebar_1"
        )
        self.btn_sidebar_2: QPushButton = self.window.findChild(
            QPushButton, "btn_sidebar_2"
        )
        self.btn_sidebar_3: QPushButton = self.window.findChild(
            QPushButton, "btn_sidebar_3"
        )
        self.header_content_title: QLabel = self.window.findChild(
            QLabel, "header_content_title"
        )
        self.main_stacked_widget = self.window.findChild(
            QStackedWidget, "main_stacked_widget"
        )

        # Connect buttons with a single function
        self.btn_sidebar_1.clicked.connect(lambda: self.change_page(0))
        self.btn_sidebar_2.clicked.connect(lambda: self.change_page(1))
        self.btn_sidebar_3.clicked.connect(lambda: self.change_page(2))

        self.load_pages()

    def load_ui_file(self):
        loader = QUiLoader()
        ui_main_path = generate_ui_file_path("main_view.ui")
        ui_main_file = QFile(ui_main_path)
        if not ui_main_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {ui_main_path}")
        self.window = loader.load(ui_main_file)
        ui_main_file.close()

    def load_pages(self):
        self.dashboard_page = DashboardPage()
        self.habits_page = HabitsPage()
        self.config_page = ConfigPage()

        self.main_stacked_widget.addWidget(self.dashboard_page.window)
        self.main_stacked_widget.addWidget(self.habits_page.window)
        self.main_stacked_widget.addWidget(self.config_page.window)

    def change_page(self, index: int):
        match index:
            case 0: self.change_header_content_title("Dashboard")
            case 1: self.change_header_content_title("Hábitos")
            case 2: self.change_header_content_title("Configuración")
        self.main_stacked_widget.setCurrentIndex(index)

    def change_header_content_title(self, title: str):
        self.header_content_title.setText(title)


class UiStarter:
    @classmethod
    def start(self):
        app = QApplication([])
        app_ui = MainWindow()
        app_ui.change_page(0)  # Show dashboard by default
        app_ui.window.show()
        app.exec()
