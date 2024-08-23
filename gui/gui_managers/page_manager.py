# gui.managers.page_manager.py : Refactored for modularity and extensibility
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from gui.list_tasks import ListTasks
from gui.create_task_page import CreateTaskDialog
from gui.ui_elements.button_elements import CustomButtons


class PageManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.pages = self.create_pages()

    def create_pages(self) -> dict:
        """Create and return a dictionary of all page names and widgets."""
        pages = {
            "Hem": self.create_home_page(),
            "Skapa Uppdrag": None,  # Delay creation until needed
            "Uppdrag": self.create_tasks_page(),
        }
        print(f"Pages initialized: {list(pages.keys())}")
        return pages

    def create_home_page(self) -> QWidget:
        """Skapa sidan för "Hem"."""
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)

        logo_label = QLabel(self.main_window)
        pixmap = QPixmap("assets/logo_to_end_all_logos.png")  # Ensure the logo is in the 'assets' folder
        scaled_pixmap = pixmap.scaled(800, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

#        welcome_label = QLabel("")
#        welcome_label.setFont(QFont("Arial", 20, QFont.Bold))
#        welcome_label.setStyleSheet("color: #0078d7;")
#        welcome_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(logo_label)
#        layout.addWidget(welcome_label)
        layout.setAlignment(Qt.AlignCenter)

        # Add the CustomButtons layout to the page
        buttons_layout = CustomButtons(self.main_window.navigation_manager)
        layout.addLayout(buttons_layout)

        return home_widget

    def create_tasks_page(self) -> QWidget:
        """Skapa sidan för "Uppdrag"."""
        return ListTasks(self.main_window, self.main_window.event_manager)

    def create_create_task_page(self) -> CreateTaskDialog:
        """Create the Create Task page."""
        # Check if the page is None to create a new instance
        if self.pages.get("Skapa Uppdrag") is None:
            print("Creating 'Skapa Uppdrag' page")

            # Create the page
            create_task_page = CreateTaskDialog(self.main_window)
            # Add the page to the pages dictionary
            self.pages["Skapa Uppdrag"] = create_task_page
            # Add the page to the stacked widget or layout if necessary
            self.main_window.stacked_widget.addWidget(create_task_page)
        return self.pages["Skapa Uppdrag"]

   # def handle_task_creation(self):
   #     """Handle the task creation event."""
   #     create_task_page = self.pages.get("Skapa Uppdrag")
   #     if create_task_page is not None:
   #         print("Task created successfully!")
   #         # Call the submit method safely
   #         create_task_page.submit()
   #         self.main_window.display_page("Uppdrag")
   #     else:
   #         print("Error: 'Skapa Uppdrag' page is not initialized!")

    def display_page(self, page_name):
        """Display the requested page by name."""
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