# gui.gui_managers.page_manager.py : Refactored for modularity and extensibility
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout  # Importera nödvändiga Qt-widgets för att bygga GUI
from PyQt5.QtGui import QPixmap  # Importera QPixmap för att hantera bilder
from PyQt5.QtCore import Qt  # Importera Qt-konstanter för alignment och andra Qt-funktioner

from ..list_tasks import ListTasks  # Importera ListTasks-sidan från en annan fil
from ..create_task_page import CreateTaskDialog  # Importera sidan för att skapa uppdrag
from ..ui_elements import CustomButtons  # Importera anpassade knappar
from ..update_task_page import UpdateTaskPage  # Importera sidan för att uppdatera uppdrag

class PageManager:
    def __init__(self, main_window, session):
        """Det här är konstruktorn för PageManager. Vi sparar huvudfönstret och sessionen som används för att visa och hantera sidor."""
        self.main_window = main_window  # Sparar en referens till huvudfönstret
        self.session = session  # Sparar en referens till databas-sessionsobjektet
        self.pages = self.create_pages()  # Skapar en dictionary där vi håller reda på alla sidor

    def create_pages(self) -> dict:
        """Skapar och returnerar en dictionary som innehåller alla sidors namn och tillhörande widgets."""
        pages = {
            "Hem": self.create_home_page(),  # Skapa startsidan och lägg till den
            "Skapa Uppdrag": None,  # Vi skapar den här sidan först när den behövs
            "Uppdrag": self.create_tasks_page(),  # Skapa sidan för att visa uppdrag
            "Uppdatera Uppdrag": UpdateTaskPage(self.main_window, self.session),  # Skapa sidan för att uppdatera uppdrag
        }
        print(f"Pages initialized: {list(pages.keys())}")  # Skriver ut vilka sidor som har initierats
        return pages

    def create_home_page(self) -> QWidget:
        """Skapar startsidan."""
        home_widget = QWidget()  # Skapar en tom widget som ska innehålla startsidan
        layout = QVBoxLayout(home_widget)  # Använder en vertikal layout för att stapla saker på varandra

        # Lägger till en logotyp på startsidan
        logo_label = QLabel(self.main_window)  # Skapar en etikett där vi kan sätta en bild
        pixmap = QPixmap("assets/logo_to_end_all_logos.png")  # Laddar bilden från assets-mappen
        scaled_pixmap = pixmap.scaled(800, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Skalar bilden till en lämplig storlek
        logo_label.setPixmap(scaled_pixmap)  # Sätter den skalade bilden på etiketten
        logo_label.setAlignment(Qt.AlignCenter)  # Centrerar bilden på sidan

        layout.addWidget(logo_label)  # Lägger till etiketten i layouten
        layout.setAlignment(Qt.AlignCenter)  # Centrerar hela layouten

        # Lägg till de anpassade knapparna på sidan
        buttons_layout = CustomButtons(self.main_window.navigation_manager)
        layout.addLayout(buttons_layout)  # Lägger till knapparna i layouten

        return home_widget  # Returnerar startsidan som vi just skapade

    def create_tasks_page(self) -> QWidget:
        """Skapar sidan för att visa uppdrag."""
        return ListTasks(self.main_window, self.session, self.main_window.event_manager)  # Returnerar en instans av ListTasks

    def create_create_task_page(self) -> CreateTaskDialog:
        """Skapar sidan för att skapa uppdrag."""
        # Kollar om sidan redan är skapad
        if self.pages.get("Skapa Uppdrag") is None:
            print("Creating 'Skapa Uppdrag' page")

            # Skapar sidan
            create_task_page = CreateTaskDialog(self.main_window)
            # Lägger till sidan i vår pages dictionary
            self.pages["Skapa Uppdrag"] = create_task_page
            # Lägger till sidan i den staplade widgeten om det behövs
            self.main_window.stacked_widget.addWidget(create_task_page)
        return self.pages["Skapa Uppdrag"]

    def display_page(self, page_name):
        """Visar sidan man begär efter namn"""
        print(f"Attempting to display page '{page_name}'")

        # Check if the page needs to be created
        if page_name == "Skapa Uppdrag" and self.pages.get(page_name) is None:
            print("Page 'Skapa Uppdrag' is None, creating it now.")
            self.pages[page_name] = self.create_create_task_page()

        page = self.pages.get(page_name)
        if page:
            index = self.main_window.stacked_widget.indexOf(page)
            if index == -1:
                self.main_window.stacked_widget.addWidget(page)
                index = self.main_window.stacked_widget.indexOf(page)
            self.main_window.stacked_widget.setCurrentIndex(index)
            print(f"Page '{page_name}' displayed at index {index}.")
        else:
            print(f"Page '{page_name}' not found. Please check if the page is correctly initialized.")


    # Lägg till fler metoder för att skapa andra sidor om det behövs