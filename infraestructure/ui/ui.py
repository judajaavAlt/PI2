from PySide6.QtWidgets import QApplication, QPushButton, QStackedWidget, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

import os
from infraestructure.ui.pages.config.config import ConfigPage
from infraestructure.ui.pages.dashboard.dashboard import DashboardPage
from infraestructure.ui.pages.habits.habits import HabitsPage
from infraestructure.ui.pages.habit_detail.habit_detail import HabitDetailPage
from infraestructure.ui.pages.habit_form.habit_form import HabitFormPage


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path


# Window class
class MainWindow:
    def __init__(self):
        self.load_ui_file()
        self.window.setWindowTitle("HabitApp")

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
        self.btn_header_content: QPushButton = self.window.findChild(
            QPushButton, "btn_header_content"
        )
        self.main_stacked_widget = self.window.findChild(
            QStackedWidget, "main_stacked_widget"
        )

        # Connect buttons with a single function
        self.btn_sidebar_1.clicked.connect(lambda: self.change_page(0))
        self.btn_sidebar_2.clicked.connect(lambda: self.change_page(1))
        self.btn_sidebar_3.clicked.connect(lambda: self.change_page(2))
        self.btn_header_content.clicked.connect(
            lambda: self.change_page(4))

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
        from PySide6.QtWidgets import QWidget, QVBoxLayout
        from PySide6.QtCore import Qt
        self.dashboard_page = DashboardPage(main_window=self)
        self.habits_page = HabitsPage(main_window=self)
        self.config_page = ConfigPage(main_window=self)
        self.habits_detail_page = HabitDetailPage(main_window=self)
        self.habits_form_page = HabitFormPage(main_window=self)

        # Aux function to create a centered container
        def centered_widget(widget):
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.addWidget(widget, alignment=Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            return container

        self.main_stacked_widget.addWidget((self.dashboard_page.window))
        self.main_stacked_widget.addWidget((self.habits_page.window))
        self.main_stacked_widget.addWidget(
            centered_widget(self.config_page.window))
        self.main_stacked_widget.addWidget(
            centered_widget(self.habits_detail_page.window))
        self.main_stacked_widget.addWidget(
            centered_widget(self.habits_form_page.window))

    def change_page(self, index: int, props: dict = None):
        match index:
            case 0:
                self.change_header_content_title("Dashboard")
                self.dashboard_page.update_widgets()
            case 1:
                self.change_header_content_title("Hábitos")
                self.habits_page.uptate()
            case 2: self.change_header_content_title("Configuración")
            case 3:
                self.change_header_content_title("Hábito: Detalle")
                self.habits_detail_page.set_props(props)
            case 4:
                self.change_header_content_title("Hábito: Formulario")
                self.habits_form_page.set_props(props)
        self.set_button_selected(index)
        self.main_stacked_widget.setCurrentIndex(index)

    def set_button_selected(self, btn_index: int):
        buttons = [self.btn_sidebar_1, self.btn_sidebar_2, self.btn_sidebar_3]

        # Styles
        normal_style = """
            QPushButton {
                background-color: white;
                color: gray;
            }
            QPushButton:hover {
                background-color: #eeeeef;
            }
            QPushButton:pressed {
                background-color: #ddddde;
            }
        """

        selected_style = """
            QPushButton {
                background-color: #d4e7f8;
                color: #007BFF;
            }
        """

        for i, btn in enumerate(buttons):
            if i == btn_index:
                btn.setStyleSheet(selected_style)
            else:
                btn.setStyleSheet(normal_style)

    def change_header_content_title(self, title: str):
        self.header_content_title.setText(title)

    def change_username(self, name: str):
        label_username: QLabel = self.window.findChild(
            QLabel, "label_username")
        label_username.setText(name)


class UiStarter:
    @classmethod
    def start(self):
        app = QApplication([])
        app_ui = MainWindow()
        app_ui.change_page(0)  # Show dashboard by default
        app_ui.window.show()
        app.exec()
