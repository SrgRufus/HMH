# gui.create_assign.py
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
)

from database.managers.assignment_manager import AssignmentManager
from utils.recurrence_utils import calculate_next_date
from database.managers.event_manager import EventManager


class CreateAssignmentDialog(QWidget):
    def __init__(self, parent, db_path: str, event_manager: EventManager):
        super().__init__(parent)
        self.main_window = parent
        self.manager = AssignmentManager(db_path=db_path, event_manager=event_manager)
        self.event_manager = EventManager

        self.setWindowTitle("Skapa Nytt Uppdrag")

        # Layouts
        main_layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Etiketter och LineEdit Widgets för obligatoriska fält.
        self.kommun_input = QLineEdit()
        self.adress_input = QLineEdit()
        self.ort_input = QLineEdit()
        self.material_dropdown = QComboBox()
        self.tomningsfrekvens_dropdown = QComboBox()

        # Lägg till 'dropdown' menyer
        self.material_dropdown.addItems(["Kartong", "Plast", "Glas", "Metall", "Tidningar"])
        self.tomningsfrekvens_dropdown.addItems([
            "Måndag, Varje vecka",
            "Tisdag, Varje vecka",
            "Onsdag, Varje vecka",
            "Torsdag, Varje vecka",
            "Fredag, Varje vecka",
            "Lördag, Varje vecka",
            "Söndag, Varje vecka",
            "Varje vecka (valfri dag)",
            "Två tillfällen varje vecka",
            "Jämn vecka",
            "Ojämn vecka",
            "Var 4:e vecka, En gång i Månaden",
            "Var 6:e vecka",
            "Var 12:e vecka",
            "Den första Torsdagen i Månaden",
            "Den 25:e varje månad"
        ])

        # Input: Obligatoriska fält
        form_layout.addWidget(QLabel("Kommun:"))
        form_layout.addWidget(self.kommun_input)
        form_layout.addWidget(QLabel("Adress:"))
        form_layout.addWidget(self.adress_input)
        form_layout.addWidget(QLabel("Ort:"))
        form_layout.addWidget(self.ort_input)
        form_layout.addWidget(QLabel("Material:"))
        form_layout.addWidget(self.material_dropdown)
        form_layout.addWidget(QLabel("Tömningsfrekvens:"))
        form_layout.addWidget(self.tomningsfrekvens_dropdown)

        # Input: Valfria fält
        self.info_input = QLineEdit()
        self.chauffor_input = QLineEdit()
        self.koordinater_input = QLineEdit()

        form_layout.addWidget(QLabel("Info:"))
        form_layout.addWidget(self.info_input)
        form_layout.addWidget(QLabel("Chaufför:"))
        form_layout.addWidget(self.chauffor_input)
        form_layout.addWidget(QLabel("Koordinater:"))
        form_layout.addWidget(self.koordinater_input)

        # Knapp: Submit/Skapa Uppdrag
        self.submit_button = QPushButton("Skapa Uppdrag")
        self.submit_button.clicked.connect(self.submit)
        button_layout.addWidget(self.submit_button)

        # Kombinerar layouts
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    # Hämta data från inputs
    def submit(self):
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

        # Validera att alla obligatoriska fält är ifyllda
        if not all([data['Kommun'], data['Adress'], data['Ort'], data['Material'], data['Tomningsfrekvens']]):
            QMessageBox.critical(self, "Fel", "Alla obligatoriska fält måste fyllas i.")
            return
            # Beräkna nästa tömningsdatum
        try:

            current_date = datetime.now()
            next_date: datetime = calculate_next_date(data['Tomningsfrekvens'], current_date)

            # Skapa uppdraget i databasen
            self.manager.create_assignment(
                kommun=data['Kommun'],
                adress=data['Adress'],
                ort=data['Ort'],
                material=data['Material'],
                tomningsfrekvens=data['Tomningsfrekvens'],
                info=data['Info'],
                chauffor=data['Chauffor'],
                koordinater=data['Koordinater'],
                next_occurrence_date=next_date  # Skicka med next_occurrence_date här
            )

            # Success! Bekräftelsemeddelande
            QMessageBox.information(self, "Uppdrag Skapat",
                                    f"Uppdraget har skapats framgångsrikt!\nNästa datum: {next_date.strftime('%Y-%m-%d')}")

            # Navigera tillbaka till huvudfönstret efter skapandet
            self.main_window.display_page("Uppdrag")

        except ValueError as e:
            QMessageBox.critical(self, "Fel", str(e))
