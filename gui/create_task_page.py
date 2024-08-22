# gui.create_task_page.py : Förbättrad version med validering och feedback användaren
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from database.managers.task_manager import TaskManager
from utils.recurrence_utils import calculate_next_date


class CreateTaskDialog(QWidget):
    def __init__(self, parent, event_manager=None):
        super().__init__(parent)
        self.main_window = parent
        self.manager = TaskManager()
        self.event_manager = event_manager  # Lagra en "event" manager för det här fönstret

        self.setWindowTitle("Skapa Nytt Uppdrag")

        main_layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Inmatningsfält
        self.kommun_input = QLineEdit()
        self.adress_input = QLineEdit()
        self.ort_input = QLineEdit()
        self.material_dropdown = QComboBox()
        self.tomningsfrekvens_dropdown = QComboBox()

        # Fyller "dropdown" menyer med val för material och tömningsfrekvens
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
            "Den första Torsdagen",
            "Den 25:e varje månad"
        ])

        # Lägg till input widgets för formuläret skapa uppdrag
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

        # Extra inmatningsfält
        self.info_input = QLineEdit()
        self.chauffor_input = QLineEdit()
        self.koordinater_input = QLineEdit()

        form_layout.addWidget(QLabel("Info:"))
        form_layout.addWidget(self.info_input)
        form_layout.addWidget(QLabel("Chaufför:"))
        form_layout.addWidget(self.chauffor_input)
        form_layout.addWidget(QLabel("Koordinater:"))
        form_layout.addWidget(self.koordinater_input)

        # Submit knapp med "klick" hanterare
        self.submit_button = QPushButton("Skapa Uppdrag")
        self.submit_button.clicked.connect(self.submit)
        button_layout.addWidget(self.submit_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)


    def submit(self):
        # Samla in data från formulär
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

        # Grundläggande feedback till användare
        if not all([data['kommun'], data['adress'], data['ort'], data['material'], data['tomningsfrekvens']]):
            QMessageBox.critical(self, "Fel", "Alla obligatoriska fält måste fyllas i.")
            return

        try:
            # Räkna ut nästa datum (next occurrence date) baserat på tömningsfrekvens
            current_date = datetime.now()
            next_date = calculate_next_date(data['tomningsfrekvens'], current_date)


            # Skapa Uppdrag
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


            # Ger feedback till användaren
            QMessageBox.information(self, "Uppdrag Skapat", f"Uppdraget har skapats framgångsrikt!\nNästa datum: {next_date.strftime('%Y-%m-%d')}")
            self.main_window.display_page("Uppdrag")


        except ValueError as e:
            QMessageBox.critical(self, "Fel", str(e))
