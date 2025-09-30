from PySide6.QtWidgets import (
    QWidget, QLabel, QListWidget, QListWidgetItem, QVBoxLayout,
    QHBoxLayout, QFrame, QSizePolicy
)
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from itertools import cycle
from PySide6.QtCore import Signal

from application.use_cases.list_habits import ListHabits
from infraestructure.persistence.habit_repository_sqlite import HabitSqliteRepository


class HabitItemWidget(QFrame):
    """
    Tarjeta de hábito estilizada con icono, texto y flecha de navegación.
    """
    def __init__(self, habit, bg_color, icon_color, parent=None):
        super().__init__(parent)

        self.setFixedHeight(70)  # altura consistente
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 6px;
            }
            QLabel {
                font-family: Arial, sans-serif;
            }
        """)

        # Efecto de sombra sutil
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 50))  # sombra suave
        self.setGraphicsEffect(shadow)

        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(12)

        # Icono circular con fondo claro y color oscuro dentro
        icon_label = QLabel()
        icon_label.setFixedSize(40, 40)
        icon_label.setStyleSheet(f"""
            background-color: {bg_color};
            border-radius: 20px;
        """)
        main_layout.addWidget(icon_label)

        # Contenedor de textos
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        # Texto principal (nombre)
        name_label = QLabel(habit.name.value)
        name_label.setStyleSheet(
            "color: #333333; font-size: 14px; font-weight: 600;")
        text_layout.addWidget(name_label)

        self.id = habit.habit_id

        # Texto secundario (ID)
        id_label = QLabel(f"ID: {habit.habit_id}")
        id_label.setStyleSheet("color: #888888; font-size: 11px;")
        text_layout.addWidget(id_label)

        main_layout.addLayout(text_layout)

        # Flecha de navegación
        arrow_label = QLabel(">")
        arrow_label.setStyleSheet("color: #CCCCCC; font-size: 16px;")
        arrow_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        main_layout.addWidget(arrow_label)

    def get_id(self):
        return self.id


class HabitsListWidget(QWidget):
    """
    Lista de hábitos estilizada tipo tarjetas.
    """
    habit_clicked = Signal(dict)  # señal que enviará {'id': habit_id}

    def __init__(self, parent=None):
        super().__init__(parent)

        self.repo = HabitSqliteRepository()
        self.list_habits_uc = ListHabits(self.repo)

        # Paleta de colores (pares: fondo claro, color oscuro para icono)
        self.color_pairs = [
            ("#E0F7FA", "#00796B"),  # azul claro + azul oscuro
            ("#FFF3E0", "#E65100"),  # naranja claro + naranja oscuro
            ("#E8F5E9", "#2E7D32"),  # verde claro + verde oscuro
            ("#F3E5F5", "#6A1B9A"),  # violeta claro + violeta oscuro
            ("#FBE9E7", "#BF360C"),  # coral claro + marrón rojizo
        ]
        self.color_cycle = cycle(self.color_pairs)

        # Layout principal
        main_layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(10)  # separación entre tarjetas
        self.list_widget.setStyleSheet(
            "QListWidget { background: #F5F5F5; border: none; }")
        main_layout.addWidget(self.list_widget)

        self.list_widget.itemClicked.connect(self.on_item_clicked)

        self.load_habits()

    def load_habits(self):
        """Carga y muestra todos los hábitos."""
        habits = self.list_habits_uc.execute()

        # Eliminar todos los widgets (si hay alguno)
        # Iteramos de atrás hacia adelante
        for i in range(self.list_widget.count() - 1, -1, -1):
            item = self.list_widget.item(i)  # Obtener el QListWidgetItem
            # Obtener el widget asociado
            widget = self.list_widget.itemWidget(item)
            if widget:
                widget.deleteLater()  # Eliminar el widget de forma segura
            self.list_widget.takeItem(i)  # Eliminar el QListWidgetItem

        if not habits:
            empty_item = QListWidgetItem("⚠️ No hay hábitos registrados.")
            self.list_widget.addItem(empty_item)
            return

        for habit in habits:
            self.add_habit(habit)

    def add_habit(self, habit):
        bg_color, icon_color = next(self.color_cycle)
        item_widget = HabitItemWidget(habit, bg_color, icon_color)

        list_item = QListWidgetItem()
        list_item.setSizeHint(item_widget.sizeHint())

        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, item_widget)

    def on_item_clicked(self, item):
        """Emitir señal con ID del hábito al hacer click en el item"""
        habit_widget = self.list_widget.itemWidget(item)
        if habit_widget:  # and hasattr(habit_widget, 'habit'):
            self.habit_clicked.emit({"id": habit_widget.get_id()})

    def update(self):
        self.load_habits()
