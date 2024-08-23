# gui.mainwindow.py : Startsida
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QStackedWidget

from database.connection import Session as DBSession
from database.managers.event_manager import EventManager
from database.managers.recurrence_manager import RecurrenceManager
from database.managers.task_manager import TaskManager

from gui.gui_managers.nav_manager import NavigationManager
from gui.gui_managers.page_manager import PageManager
from gui.ui_elements.button_elements import CustomButtons
from gui.ui_elements.search_bar import SearchBar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("HMH: Henry's Molok Hanterare")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize necessary managers first
        self.session = DBSession()
        self.recurrence_manager = RecurrenceManager()
        self.event_manager = EventManager(self.recurrence_manager)
        self.task_manager = TaskManager()

        # Step 1: Set up the stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Step 2: Initialize the NavigationManager first with a placeholder for page_manager
        self.navigation_manager = NavigationManager(self, page_manager=None)

        # Step 3: Initialize the PageManager with only the MainWindow
        self.page_manager = PageManager(self)

        # Step 4: Now that both managers are initialized, update NavigationManager with the actual PageManager
        self.navigation_manager.page_manager = self.page_manager

        # Step 5: Initialize the UI elements
        self.setup_ui()

        # Step 6: Apply dark mode to the UI
        self.apply_dark_mode()

    def setup_ui(self) -> None:
        # Create the home page and add it to the stacked widget
        home_page = self.page_manager.create_home_page()
        self.stacked_widget.addWidget(home_page)

        # Display the home page initially
        self.page_manager.display_page("Hem")

        # Insert logo on the home page
        logo_label = QLabel()
        pixmap = QPixmap("assets/remondis-logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Add the logo to the home page's layout
        home_layout = self.stacked_widget.widget(self.stacked_widget.indexOf(home_page)).layout()
        home_layout.addWidget(logo_label)

        # Create the navigation menus
        self.navigation_manager.create_menus()

    def apply_dark_mode(self):
        """Apply a dark theme to the entire application."""
        dark_palette = {
            "background-color": "#1e1e1e",
            "color": "#ffffff",
            "border-color": "#3a3a3a",
            "selection-color": "#ffffff",
            "selection-background-color": "#0078d7",
        }
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: {dark_palette["background-color"]};
                color: {dark_palette["color"]};
            }}
            QLabel {{
                color: {dark_palette["color"]};
            }}
            QMenuBar {{
                background-color: {dark_palette["background-color"]};
                color: {dark_palette["color"]};
            }}
            QMenu {{
                background-color: {dark_palette["background-color"]};
                color: {dark_palette["color"]};
            }}
            """
        )

    def _initialize_ui_elements(self, layout: QVBoxLayout) -> None:
        self.search_bar = SearchBar(self)
        layout.addLayout(self.search_bar)
        layout.addWidget(self.search_bar.search_result_label)
        self.custom_buttons = CustomButtons(self.navigation_manager)
        layout.addLayout(self.custom_buttons)
