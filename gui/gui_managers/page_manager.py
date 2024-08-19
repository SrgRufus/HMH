# gui.managers.page_manager.py
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.Qt import Qt, QFont

from gui.create_assign import CreateAssignmentDialog
from gui.list_assign import ListAssign


class PageManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.pages = {}

    def create_pages(self):
        # Skapa sidor och lägg till dem i pages-ordboken
        self.pages["Hem"] = self.create_home_page()
        self.pages["Uppdrag"] = self.create_assignments_page()
        self.pages["Skapa Uppdrag"] = self.create_create_assignment_page()
      #  self.pages["Sök uppdrag"] = QLabel("Sök uppdrag Sida"),
      #  self.pages["Inställningar"] = QLabel("Inställningar Sida"),
      #  self.pages["Historik"] = QLabel("Historik Sida"),
      #  self.pages["Statistik"] = QLabel("Statistik Sida"),

        # Lägg till fler sidor om det behövs
        return self.pages

    @staticmethod
    def create_home_page() -> QWidget:
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)

        welcome_label = QLabel("Välkommen till Henry's Molok Hanterare, eller HMH (Patent pending)")
        welcome_label.setFont(QFont("Arial", 16, QFont.Bold))
        welcome_label.setStyleSheet("color: #2E8B57;")
        welcome_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(welcome_label)
        return home_widget

    def create_assignments_page(self) -> QWidget:
        # Logik för att skapa Uppdrag-sidan
        assignments_page = ListAssign(self.main_window, self.main_window.db_path, self.main_window.event_manager)
        return assignments_page

    def create_create_assignment_page(self) -> QWidget:
        # Logik för att skapa "Skapa Uppdrag"-sidan
        create_assign_page = CreateAssignmentDialog(self.main_window, self.main_window.db_path, self.main_window.event_manager)
        return create_assign_page

    # Lägg till fler metoder för att skapa andra sidor om det behövs
