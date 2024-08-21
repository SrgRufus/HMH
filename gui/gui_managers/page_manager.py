# gui.managers.page_manager.py
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.Qt import Qt, QFont

from gui.create_task import CreateTaskDialog
from gui.list_tasks import ListTasks


class PageManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.pages = {}

    def create_pages(self):
        # Skapa sidor och lägg till dem i pages-ordboken
        self.pages["Hem"] = self.create_home_page()
        self.pages["Uppdrag"] = self.create_tasks_page()
        self.pages["Skapa Uppdrag"] = self.create_create_task_page()
        self.pages["Ändra Uppdrag"] = self.edit_task()

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

    def create_tasks_page(self) -> QWidget:
        # Logik för att skapa Uppdrag-sidan
        tasks_page = ListTasks(self.main_window, self.main_window.db_path, self.main_window.event_manager)
        return tasks_page

    def create_create_task_page(self) -> QWidget:
        # Logik för att skapa "Skapa Uppdrag"-sidan
        create_task_page = CreateTaskDialog(self.main_window, self.main_window.db_path, self.main_window.event_manager)
        return create_task_page

    def edit_task(self) -> QWidget:
        edit_task = EditTask(self.edit_task, self.edit_task.db_path, self.edit_task.event_manager)
        return edit_task
    # Lägg till fler metoder för att skapa andra sidor om det behövs
