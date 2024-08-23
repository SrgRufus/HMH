# gui.create_task_page.py : Förbättrad version med validering och feedback användaren
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QGridLayout
)
from database.managers.task_manager import TaskManager
from utils.recurrence_utils import calculate_next_date


class CreateTaskDialog(QWidget):

    def __init__(self, parent, event_manager=None):
        super().__init__(parent)
        self.main_window = parent
        self.manager = TaskManager()
        self.event_manager = event_manager  # Lagra en "event" manager för det här fönstret

        self.setWindowTitle("Skapa Uppdrag")
        self.setMinimumSize(400, 300)  # Adjust the size as needed

        main_layout = QGridLayout()


        # Inmatningsfält
        self.kommun_input = QLineEdit()
        self.adress_input = QLineEdit()
        self.ort_input = QLineEdit()
        self.material_dropdown = QComboBox()
        self.tomningsfrekvens_dropdown = QComboBox()

        # Valfria Inmatningar
        self.info_input = QLineEdit()  # Initialize info_input
        self.chauffor_input = QLineEdit()  # Initialize chauffor_input
        self.koordinater_input = QLineEdit()  # Initialize koordinater_input

        # Fyller "dropdown" menyer med val för material och tömningsfrekvens
        self.material_dropdown.addItems([
            "Kartong", "Plast", "Glas",
             "Metall", "Tidningar"
        ])
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

        # Adding widgets to the grid layout
        main_layout.addWidget(QLabel("Kommun:"), 0, 0)
        main_layout.addWidget(self.kommun_input, 0, 1, 1, 2)  # Spanning 2 columns

        main_layout.addWidget(QLabel("Adress:"), 1, 0)
        main_layout.addWidget(self.adress_input, 1, 1, 1, 2)

        main_layout.addWidget(QLabel("Ort:"), 2, 0)
        main_layout.addWidget(self.ort_input, 2, 1, 1, 2)

        main_layout.addWidget(QLabel("Material:"), 3, 0)
        main_layout.addWidget(self.material_dropdown, 3, 1, 1, 2)

        main_layout.addWidget(QLabel("Tömningsfrekvens:"), 4, 0)
        main_layout.addWidget(self.tomningsfrekvens_dropdown, 4, 1, 1, 2)

        main_layout.addWidget(QLabel("Info:"), 5, 0)
        main_layout.addWidget(self.info_input, 5, 1, 1, 2)

        main_layout.addWidget(QLabel("Chaufför:"), 6, 0)
        main_layout.addWidget(self.chauffor_input, 6, 1)

        main_layout.addWidget(QLabel("Koordinater:"), 6, 2)
        main_layout.addWidget(self.koordinater_input, 6, 3)

        # Create the QPushButton first
        self.submit_button = QPushButton("Skapa Nytt Uppdrag")

        # Add the button to the layout
        main_layout.addWidget(self.submit_button, 7, 0, 1, 4)

        # Now, connect the clicked signal to the submit method
        self.submit_button.clicked.connect(self.submit)

        # Submit button
        self.submit_button.clicked.connect(self.submit)
        self.submit_button = QPushButton("Skapa Nytt Uppdrag")
        main_layout.addWidget(self.submit_button, 7, 0, 1, 4)  # Span across the entire width

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
