from PySide6.QtWidgets import QLineEdit, QPlainTextEdit, QCheckBox, QPushButton, QLabel, QGraphicsColorizeEffect
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QPropertyAnimation, QEasingCurve
from application.controllers.habit_controller import HabitController
from PySide6.QtGui import QColor
import os


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    ui_path = os.path.join(base_dir, file)
    return ui_path


class HabitFormPage:
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.props = None
        self.load_ui_file()
        self.controller = HabitController()

        # Get elements
        self.name_edit: QLineEdit = self.window.findChild(
            QLineEdit, "lineEdit_name")
        self.desc_edit: QPlainTextEdit = self.window.findChild(
            QPlainTextEdit, "plainText_desc")
        self.monday_check: QCheckBox = self.window.findChild(
            QCheckBox, "checkBox_1")
        self.tuesday_check: QCheckBox = self.window.findChild(
            QCheckBox, "checkBox_2")
        self.wednesday_check: QCheckBox = self.window.findChild(
            QCheckBox, "checkBox_3")
        self.thursday_check: QCheckBox = self.window.findChild(
            QCheckBox, "checkBox_4")
        self.friday_check: QCheckBox = self.window.findChild(
            QCheckBox, "checkBox_5")
        self.saturday_check: QCheckBox = self.window.findChild(
            QCheckBox, "checkBox_6")
        self.sunday_check: QCheckBox = self.window.findChild(
            QCheckBox, "checkBox_7")
        self.save_button: QPushButton = self.window.findChild(
            QPushButton, "btn_save")
        self.cancel_button: QPushButton = self.window.findChild(
            QPushButton, "btn_cancel")

        self.checks = [
            self.monday_check, self.tuesday_check, self.wednesday_check,
            self.thursday_check, self.friday_check, self.saturday_check,
            self.sunday_check]

        # Connect button
        self.save_button.clicked.connect(self.save_habit)
        self.cancel_button.clicked.connect(self.go_back)

    def load_ui_file(self):
        loader = QUiLoader()
        page_ui_path = generate_ui_file_path("habit_form_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()

    def set_props(self, props: dict | None):
        self.clean_form()
        self.props = props
        if self.props:
            id = props["id"]
            habit_props = self.controller.get_habit(id)
            self.show_edit_view(habit_props)
        else:
            self.show_create_view()

    # Views logic
    def show_edit_view(self, habit_props):
        # Set title
        label_title: QLabel = self.window.findChild(QLabel, "label_title")
        label_title.setText("Editando hábito")
        # Set habit props in fields
        self.name_edit.setText(str(habit_props.name))
        self.desc_edit.setPlainText(str(habit_props.description))
        freq_array = habit_props.frequency.value

        for i, value in enumerate(freq_array):
            self.checks[i].setChecked(bool(value))

    def show_create_view(self):
        # Set title
        label_title: QLabel = self.window.findChild(QLabel, "label_title")
        label_title.setText("Nuevo hábito")

    def save_habit(self):
        name = self.name_edit.text()
        desc = self.desc_edit.toPlainText()
        frequency = self.get_active_checks()
        habit_id = None

        if not self.check_fields(name, desc, frequency):
            return

        if self.props:
            habit_id = self.props["id"]
            habit_props = self.controller.get_habit(habit_id)
            habit_props.modify(name, desc, frequency)
            self.controller.update_habit(habit_props)
        else:
            habit_id = self.controller.create_habit(name, desc, frequency)

        self.props = {"id": habit_id}
        self.go_back()

    # Get a list of 0's and 1's to see which checks are checked
    def get_active_checks(self):
        return [1 if checkbox.isChecked() else 0 for checkbox in self.checks]

    def clean_form(self):
        # Clean elements
        self.props = None
        self.name_edit.setText("")
        self.desc_edit.setPlainText("")

        for check in self.checks:
            check.setChecked(False)

        self.show_message(
            "Puedes editar o eliminar"
            " este hábito luego en la sección de Hábitos: Detalle")

    # If has id, then it was editing, so go back to detail page,
    # else go back to dashboard
    def go_back(self):
        if self.props:
            self.main_window.change_page(3, self.props)
        else:
            self.main_window.change_page(0)

    def check_fields(self, name, description, frequency):
        if len(name) < 1:
            self.show_message("Por favor ingrese un nombre")
            return False
        if len(description) < 1:
            self.show_message("Por favor ingrese una descripción")
            return False
        if not any(frequency):
            self.show_message("Por favor seleccione al menos un día")
            return False
        if not self.props:
            if not self.is_habit_name_unique(name):
                return False
        else:
            habit_props = self.controller.get_habit(self.props["id"])
            if habit_props.name.value.lower() != name.lower():
                if not self.is_habit_name_unique(name):
                    return False

        return True

    # Show a message to the user with a pulse color animation
    def show_message(self, message):
        label_message: QLabel = self.window.findChild(QLabel, "label_message")
        label_message.setText(message)

        # If there is no effect, create it
        if not hasattr(label_message, "color_effect"):
            effect = QGraphicsColorizeEffect()
            label_message.setGraphicsEffect(effect)
            label_message.color_effect = effect

        effect = label_message.color_effect

        # Create or reuse animation
        if not hasattr(label_message, "pulse_anim"):
            anim = QPropertyAnimation(effect, b"color")
            anim.setDuration(1500)
            anim.setStartValue(QColor("black"))
            anim.setKeyValueAt(0, QColor("#AA0000"))
            anim.setEndValue(QColor("black"))
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            label_message.pulse_anim = anim

        # Restart animation
        anim = label_message.pulse_anim
        anim.stop()
        anim.start()

    def is_habit_name_unique(self, name):
        if self.controller.get_habit_name_existence(name):
            self.show_message(
                "Ya existe un hábito con ese nombre."
                " Por favor, elija otro")
            return False
