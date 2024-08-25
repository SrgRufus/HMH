# gui/create_task_page.py

from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox,
    QGraphicsDropShadowEffect, QVBoxLayout,
    QGridLayout, QWidget, QSizePolicy
)

from database.managers import TaskManager
from utils import calculate_next_date
from .resize_manager import ResizeManager

class CreateTaskDialog(QDialog):
    def __init__(self, parent, event_manager=None):
        super().__init__(parent)
        self.main_window = parent
        self.task_manager = TaskManager()
        self.event_manager = event_manager

        self.resize_manager = ResizeManager()

        self.setWindowTitle("Skapa Uppdrag")
        self.setMinimumSize(400, 300)

        # Shadow effect for the entire widget
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setOffset(10, 10)
        self.setGraphicsEffect(shadow_effect)

        # Create the main layout with vertical stacking
        main_layout = QVBoxLayout(self)

        # Frame label for the background image
        self.frame_label = QLabel(self)
        pixmap = QPixmap("assets/dalle_frame.png")
        self.frame_label.setPixmap(pixmap)
        self.frame_label.setScaledContents(True)
        main_layout.addWidget(self.frame_label)

        # Widget to hold inputs, placed inside the frame label
        input_widget = QWidget(self.frame_label)
        input_layout = QGridLayout(input_widget)
        input_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins if necessary

        # Kommun input
        self.kommun_label = QLabel("Kommun", input_widget)
        self.kommun_input = QLineEdit(input_widget)
        input_layout.addWidget(self.kommun_label, 0, 0)
        input_layout.addWidget(self.kommun_input, 1, 0)

        # Adress input
        self.adress_label = QLabel("Adress", input_widget)
        self.adress_input = QLineEdit(input_widget)
        input_layout.addWidget(self.adress_label, 0, 1)
        input_layout.addWidget(self.adress_input, 1, 1, 1, 2)

        # Ort input
        self.ort_label = QLabel("Ort", input_widget)
        self.ort_input = QLineEdit(input_widget)
        input_layout.addWidget(self.ort_label, 0, 3)
        input_layout.addWidget(self.ort_input, 1, 3)

        # Chauffor input
        self.chauffor_label = QLabel("Chaufför", input_widget)
        self.chauffor_input = QLineEdit(input_widget)
        input_layout.addWidget(self.chauffor_label, 0, 4)
        input_layout.addWidget(self.chauffor_input, 1, 4)

        # Tömningsfrekvens dropdown
        self.tomningsfrekvens_label = QLabel("Tömningsfrekvens", input_widget)
        self.tomningsfrekvens_dropdown = QComboBox(input_widget)
        self.tomningsfrekvens_dropdown.addItems([
            "Måndag, Varje vecka", "Tisdag, Varje vecka", "Onsdag, Varje vecka",
            "Torsdag, Varje vecka", "Fredag, Varje vecka", "Lördag, Varje vecka",
            "Söndag, Varje vecka", "Varje vecka (valfri dag)",
            "Två tillfällen varje vecka", "Jämn vecka", "Ojämn vecka",
            "Var 4:e vecka, En gång i Månaden", "Var 6:e vecka",
            "Var 12:e vecka", "Den första Torsdagen", "Den 25:e varje månad"
        ])
        input_layout.addWidget(self.tomningsfrekvens_label, 2, 0)
        input_layout.addWidget(self.tomningsfrekvens_dropdown, 3, 0)

        # Material dropdown
        self.material_label = QLabel("Material", input_widget)
        self.material_dropdown = QComboBox(input_widget)
        self.material_dropdown.addItems(["Kartong", "Plast", "Glas", "Metall", "Tidningar"])
        input_layout.addWidget(self.material_label, 2, 1)
        input_layout.addWidget(self.material_dropdown, 3, 1)

        # Koordinater input
        self.koordinater_label = QLabel("Koordinater", input_widget)
        self.koordinater_input = QLineEdit(input_widget)
        input_layout.addWidget(self.koordinater_label, 2, 2)
        input_layout.addWidget(self.koordinater_input, 3, 2)

        # Info input (multi-line)
        self.info_label = QLabel("Info", input_widget)
        self.info_input = QLineEdit(input_widget)
        self.info_input.setMinimumHeight(60)  # Increase height for multi-line input
        input_layout.addWidget(self.info_label, 4, 0, 1, 5)
        input_layout.addWidget(self.info_input, 5, 0, 1, 5)

        # Submit button
        self.submit_button = QPushButton("Skapa Nytt Uppdrag", self)
        main_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        # Apply stylesheet
        self.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: #4d4d4d;
                border: 2px solid #666;
                border-radius: 10px;
                padding: 5px;
                color: #ffffff;
            }
            QLineEdit:hover, QComboBox:hover {
                border: 2px solid #a9a9a9;
            }
            QPushButton {
                background-color: #5a5a5a;
                border: 2px solid #7f7f7f;
                border-radius: 10px;
                padding: 10px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #787878;
                border: 2px solid #a9a9a9;
            }
        """)

        # Apply resize policies
        self._apply_resize_policies()

        self.setLayout(main_layout)

    def _apply_resize_policies(self):
        """Apply resize policies to input fields and layout."""
        input_widgets = [
            self.kommun_input, self.adress_input, self.ort_input,
            self.chauffor_input, self.tomningsfrekvens_dropdown,
            self.material_dropdown, self.koordinater_input, self.info_input
        ]

        for widget in input_widgets:
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.info_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, event):
        """Handle resize event and delegate to ResizeManager."""
        self.resize_manager.resize_create_task_dialog(self)
        super().resizeEvent(event)

    def submit(self):
        # Collect data from form
        data = {
            'kommun': self.kommun_input.text(),
            'adress': self.adress_input.text(),
            'ort': self.ort_input.text(),
            'material': self.material_dropdown.currentText(),
            'tomningsfrekvens': self.tomningsfrekvens_dropdown.currentText(),
            'info': self.info_input.text(),
            'chauffor': self.chauffor_input.text(),
            'koordinater': self.koordinater_input.text()
        }

        if not all([data['kommun'], data['adress'], data['ort'], data['material'], data['tomningsfrekvens']]):
            QMessageBox.critical(self, "Fel", "Alla obligatoriska fält måste fyllas i.")
            return

        try:
            current_date = datetime.now()
            next_date = calculate_next_date(data['tomningsfrekvens'], current_date)
            self.manager.create_task(
                kommun=data['kommun'],
                adress=data['adress'],
                ort=data['ort'],
                material=data['material'],
                tomningsfrekvens=data['tomningsfrekvens'],
                info=data['info'],
                chauffor=data['chauffor'],
                koordinater=data['koordinater'],
                next_occurrence_date=next_date
            )
            QMessageBox.information(self, "Uppdrag Skapat", f"Uppdraget har skapats framgångsrikt!\nNästa datum: {next_date.strftime('%Y-%m-%d')}")
            self.main_window.display_page("Uppdrag")
        except ValueError as e:
            QMessageBox.critical(self, "Fel", str(e))
