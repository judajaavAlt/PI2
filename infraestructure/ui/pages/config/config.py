# ui/config_page.py
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox, QPushButton, QLabel, QLineEdit, QToolButton
from PySide6.QtGui import QPixmap
import os

from infraestructure.repositories.preferences_user_repository import PreferencesUserRepository
from application.use_cases.update_profile_use_case import UpdateProfileUseCase


def generate_ui_file_path(file: str):
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, file)


class ConfigPage:
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.load_ui_file()
        self.repo = PreferencesUserRepository()
        self.use_case = UpdateProfileUseCase(self.repo)
        self.photo_path = ""

        # buscar widgets por objectName (más fiable con QUiLoader)
        self.save_btn = self.window.findChild(QPushButton, "saveButton")
        self.cancel_btn = self.window.findChild(QPushButton, "cancelButton")
        self.load_img_btn = self.window.findChild(QToolButton, "loadImageButton")
        self.image_label = self.window.findChild(QLabel, "imageLabel")
        self.name_input = self.window.findChild(QLineEdit, "nameLineEdit")

        # Conectar señales
        if self.save_btn:
            self.save_btn.clicked.connect(self.on_save)
        if self.cancel_btn:
            self.cancel_btn.clicked.connect(self.on_cancel)
        if self.load_img_btn:
            self.load_img_btn.clicked.connect(self.on_load_image)

        # Cargar datos existentes
        self.load_existing()

    def load_ui_file(self):
        loader = QUiLoader()
        page_ui_path = generate_ui_file_path("config_view.ui")
        page_file = QFile(page_ui_path)
        if not page_file.open(QFile.ReadOnly):
            raise RuntimeError(f"No pudo abrir el archivo en: {page_ui_path}")
        self.window = loader.load(page_file)
        page_file.close()

    def load_existing(self):
        profile = self.use_case.load()
        if profile:
            if self.name_input:
                self.name_input.setText(profile.name)
                self.main_window.change_username(profile.name)
            if profile.photo_path:
                self.photo_path = profile.photo_path
                self.set_image(profile.photo_path)

    def set_image(self, path):
        pix = QPixmap(path)
        if not pix.isNull() and self.image_label:
            # Crear un pixmap circular
            size = 120  # Tamaño del círculo
            rounded_pix = QPixmap(size, size)
            rounded_pix.fill(Qt.transparent)
            
            # Crear un painter para dibujar el círculo
            from PySide6.QtGui import QPainter, QBrush
            from PySide6.QtCore import QRect
            painter = QPainter(rounded_pix)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Crear un path circular para el clip
            from PySide6.QtGui import QPainterPath
            path = QPainterPath()
            path.addEllipse(0, 0, size, size)
            painter.setClipPath(path)
            
            # Escalar la imagen para que llene el círculo manteniendo la relación de aspecto
            scaled = pix.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            # Centrar la imagen en el círculo
            x = (scaled.width() - size) / 2
            y = (scaled.height() - size) / 2
            painter.drawPixmap(QRect(0, 0, size, size), scaled, QRect(x, y, size, size))
            
            painter.end()
            
            self.image_label.setPixmap(rounded_pix)
        elif self.image_label:
            self.image_label.setText("No image")

    def on_load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self.window, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            self.photo_path = file_path
            self.set_image(file_path)

    def on_save(self):
        name = self.name_input.text().strip() if self.name_input else ""
        photo = self.photo_path or ""
        self.main_window.change_username(name)
        self.use_case.execute(name, photo)
        QMessageBox.information(self.window, "Guardado", "Perfil actualizado correctamente")
        

    def on_cancel(self):
        QMessageBox.information(self.window, "No guardado", "Los cambios en el perfil no han sido guardados")
