# gui/create_task_page.py
import logging
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox,
    QGraphicsDropShadowEffect, QVBoxLayout,
    QGridLayout, QWidget, QSizePolicy
)

from database import TaskManager
from utils import calculate_next_date
from .resize_manager import ResizeManager

class CreateTaskDialog(QDialog):
    def __init__(self, parent, event_manager=None):
        """Konstruktor för att skapa ett dialogfönster för att skapa nya uppdrag."""
        super().__init__(parent)
        self.main_window = parent  # Referens till huvudfönstret
        self.task_manager = TaskManager(self.main_window.session)  # Instansierar TaskManager med nuvarande session
        self.event_manager = event_manager  # Eventuell händelsehanterare (kan vara None)

        self.resize_manager = ResizeManager()  # Initierar ResizeManager för att hantera storleksändring

        self.setWindowTitle("Skapa Uppdrag")  # Sätter dialogfönstrets titel
        self.setMinimumSize(400, 300)  # Sätter minsta storlek på dialogen

        # Skugg effekt för hela widgeten
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setOffset(10, 10)
        self.setGraphicsEffect(shadow_effect)

        # Skapa huvudlayouten med vertikal stapling
        main_layout = QVBoxLayout(self)

        # Rametikett (QLabel) för bakgrundsbilden
        self.frame_label = QLabel(self)
        pixmap = QPixmap("assets/dalle_frame.png")
        self.frame_label.setPixmap(pixmap)
        self.frame_label.setScaledContents(True)  # Ser till att bilden skalas inuti QLabel
        main_layout.addWidget(self.frame_label)

        # Widget för att hålla inputs (formulär), placerad inuti rametiketten
        input_widget = QWidget(self.frame_label)
        input_layout = QGridLayout(input_widget)
        input_layout.setContentsMargins(10, 10, 10, 10)  # Justerar marginaler om nödvändigt

        # Kommun "input" - (Obligatorisk)
        self.kommun_label = QLabel("Kommun", input_widget)
        self.kommun_input = QLineEdit(input_widget)
        input_layout.addWidget(self.kommun_label, 0, 0)
        input_layout.addWidget(self.kommun_input, 1, 0)

        # Adress "input" - (Obligatorisk)
        self.adress_label = QLabel("Adress", input_widget)
        self.adress_input = QLineEdit(input_widget)
        input_layout.addWidget(self.adress_label, 0, 1)
        input_layout.addWidget(self.adress_input, 1, 1, 1, 2)

        # Ort "input" - (Obligatorisk)
        self.ort_label = QLabel("Ort", input_widget)
        self.ort_input = QLineEdit(input_widget)
        input_layout.addWidget(self.ort_label, 0, 3)
        input_layout.addWidget(self.ort_input, 1, 3)

        # Chaufför "input"
        self.chauffor_label = QLabel("Chaufför", input_widget)
        self.chauffor_input = QLineEdit(input_widget)
        input_layout.addWidget(self.chauffor_label, 0, 4)
        input_layout.addWidget(self.chauffor_input, 1, 4)

        # Tömningsfrekvens "dropdown"-meny - (Obligatorisk)
        self.tomningsfrekvens_label = QLabel("Tömningsfrekvens", input_widget)
        self.tomningsfrekvens_dropdown = QComboBox(input_widget)
        self.tomningsfrekvens_dropdown.addItems([
            "Måndag, Varje vecka", "Tisdag, Varje vecka", "Onsdag, Varje vecka",
            "Torsdag, Varje vecka", "Fredag, Varje vecka", "Lördag, Varje vecka",
            "Söndag, Varje vecka", "Varje vecka (valfri dag)",
            "Två tillfällen varje vecka", "Jämn vecka", "Ojämn vecka",
            "Var 4:e vecka, En gång i Månaden", "Var 6:e vecka",
            "Var 12:e vecka", "Den första Torsdagen", "Den 25:e varje månad"
        ])  # Lägg till alternativ för tömningsfrekvens
        input_layout.addWidget(self.tomningsfrekvens_label, 2, 0)
        input_layout.addWidget(self.tomningsfrekvens_dropdown, 3, 0)

        # Material "dropdown"-meny - (Obligatorisk)
        self.material_label = QLabel("Material", input_widget)
        self.material_dropdown = QComboBox(input_widget)
        self.material_dropdown.addItems(["Kartong", "Plast", "Glas", "Metall", "Tidningar"])
        input_layout.addWidget(self.material_label, 2, 1)
        input_layout.addWidget(self.material_dropdown, 3, 1)

        # Koordinater "input"
        self.koordinater_label = QLabel("Koordinater", input_widget)
        self.koordinater_input = QLineEdit(input_widget)
        input_layout.addWidget(self.koordinater_label, 2, 2)
        input_layout.addWidget(self.koordinater_input, 3, 2)

        # Info "input"-(multi-line)
        self.info_label = QLabel("Info", input_widget)
        self.info_input = QLineEdit(input_widget)
        self.info_input.setMinimumHeight(60)  # Ökar höjden för att möjliggöra flerradig input
        input_layout.addWidget(self.info_label, 4, 0, 1, 5)
        input_layout.addWidget(self.info_input, 5, 0, 1, 5)

        # "Skapa Uppdrag" knapp
        self.submit_button = QPushButton("Skapa Nytt Uppdrag", self)
        main_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)
        # Koppla knappen till submit-funktionen
        self.submit_button.clicked.connect(self.submit)

        # Applicera "stylesheet". (Utseende)
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
        """)  # Ställ in stilen för hela dialogen

        # Använd policyer för storleksändring
        self._apply_resize_policies()

        self.setLayout(main_layout)

    def _apply_resize_policies(self):
        """Tillämpa policyer för ändra storlek på inmatningsfält och layout."""
        input_widgets = [
            self.kommun_input, self.adress_input, self.ort_input,
            self.chauffor_input, self.tomningsfrekvens_dropdown,
            self.material_dropdown, self.koordinater_input, self.info_input
        ]

        for widget in input_widgets:
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Expanderar horisontellt men fixerar vertikalt

        self.info_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Expanderar i båda riktningar

    def resizeEvent(self, event):
        """Hantera resize-händelse och delegera till ResizeManager."""
        self.resize_manager.resize_create_task_dialog(self)
        super().resizeEvent(event)

    def submit(self):
        """
        Hanterar inskickning av data för att skapa ett nytt uppdrag.
        """
        logging.debug("Submit method called.")
        try:
            # 1. Samla in data från inmatningsfälten
            kommun = self.kommun_input.text().strip()
            adress = self.adress_input.text().strip()
            ort = self.ort_input.text().strip()
            material = self.material_dropdown.currentText().strip()
            tomningsfrekvens = self.tomningsfrekvens_dropdown.currentText().strip()
            info = self.info_input.text().strip()
            chauffor = self.chauffor_input.text().strip()
            koordinater = self.koordinater_input.text().strip()

            logging.debug("Collected input data from form fields.")

            # 2. Validera obligatoriska fält
            if not all([kommun, adress, ort, material, tomningsfrekvens]):
                logging.warning("Ett eller flera obligatoriska fält är tomma.")
                QMessageBox.warning(self, "Valideringsfel", "Vänligen fyll i alla obligatoriska fält.")
                return

            # 3. Beräkna nästa förekomstdatum baserat på tomningsfrekvens
            try:
                current_date = datetime.now()
                next_occurrence_date = calculate_next_date(tomningsfrekvens, current_date)
                logging.debug(f"Next occurrence date calculated: {next_occurrence_date}")
            except ValueError as ve:
                logging.error(f"Fel vid beräkning av nästa datum: {ve}")
                QMessageBox.critical(self, "Beräkningsfel",
                                     f"Kunde inte beräkna nästa datum för den valda frekvensen: {ve}")
                return

            # 4. Skapa data-dictionary för uppdraget
            task_data = {
                'kommun': kommun,
                'adress': adress,
                'ort': ort,
                'material': material,
                'tomningsfrekvens': tomningsfrekvens,
                'info': info,
                'chauffor': chauffor,
                'koordinater': koordinater,
                'next_occurrence_date': next_occurrence_date,  # Här skickar vi nu ett datetime-objekt
                'status': 'Aktiv'
            }

            logging.debug(f"Prepared task data for creation: {task_data}")

            # 5. Initiera TaskManager för att referera till metoden "create_task" och försök skapa uppdraget
            task_manager = TaskManager(self.main_window.session)
            success = task_manager.create_task(task_data)

            # 6. Ge feedback till användaren baserat på resultatet
            if success:
                logging.info("Uppdraget skapades framgångsrikt.")
                QMessageBox.information(self, "Framgång", "Uppdraget har skapats framgångsrikt!")
                self.close()  # Stänger dialogen efter framgångsrik skapelse
            else:
                logging.error("Misslyckades med att skapa uppdraget.")
                QMessageBox.critical(self, "Fel", "Ett fel uppstod vid skapandet av uppdraget. Vänligen försök igen.")

        except Exception as e:
            logging.exception(f"Ett oväntat fel uppstod i submit-metoden: {e}")
            QMessageBox.critical(self, "Oväntat fel", f"Ett oväntat fel uppstod: {str(e)}")
