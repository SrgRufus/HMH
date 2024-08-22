# gui.managers.page_manager.py : Refactored for modularity and extensibility
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from gui.list_tasks import ListTasks
from gui.create_task_page import CreateTaskDialog


class PageManager:
    def __init__(self, main_window):
        self.main_window = main_window


    def create_pages(self):
        """Skapa och returnera en ordbok på alla namnen på sidorna"""
        pages = {
            "Hem": self.create_home_page(),
            "Skapa Uppdrag": self.create_create_task_page(),
            "Uppdrag": self.create_tasks_page(),
        }
        print("Pages created:", pages.keys()) #Debug print
        return pages


    def create_home_page(self) -> QWidget:
        """Skapa sidan för "Hem"."""
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)

        logo_label = QLabel(self.main_window)
        pixmap = QPixmap("assets/final_super_rad_logo.png")  # Ensure the logo is in the 'assets' folder

        scaled_pixmap = pixmap.scaled(1600, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)


        welcome_label = QLabel("Välkommen till Henry's Molok Hanterare, eller HMH (Patent pending)")
        welcome_label.setFont(QFont("Arial", 20, QFont.Bold))
        welcome_label.setStyleSheet("color: #0078d7;")
        welcome_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(logo_label)
        layout.addWidget(welcome_label)
        layout.setAlignment(Qt.AlignCenter)
        return home_widget

    def create_tasks_page(self) -> QWidget:
            """Skapa sidan för "Uppdrag"."""
            return ListTasks(self.main_window, self.main_window.event_manager)


    def create_create_task_page(self) -> QWidget:
        """Skapa sidan för att "Skapa Uppdrag"."""
        return CreateTaskDialog(self.main_window, self.main_window.event_manager)

    # Lägg till fler metoder för att skapa andra sidor om det behövs