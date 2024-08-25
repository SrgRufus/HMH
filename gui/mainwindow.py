# gui/mainwindow.py
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QStackedWidget

from database import EventManager, RecurrenceManager, TaskManager, Session as DBSession
from .gui_managers import NavigationManager, PageManager
from .ui_elements import CustomButtons, SearchBar
from .resize_manager import ResizeManager

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("HMH: Henry's Molok Hanterare")
        self.setGeometry(100, 100, 1200, 800)

        self.resize_manager = ResizeManager()  # Initialize ResizeManager

        # Initialize necessary managers first
        self.session = DBSession()
        self.recurrence_manager = RecurrenceManager()
        self.event_manager = EventManager(self.recurrence_manager)
        self.task_manager = TaskManager()

        # Set up the stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize the NavigationManager first with a placeholder for page_manager
        self.navigation_manager = NavigationManager(self, page_manager=None)

        # Initialize the PageManager with only the MainWindow
        self.page_manager = PageManager(self)

        # Now that both managers are initialized, update NavigationManager with the actual PageManager
        self.navigation_manager.page_manager = self.page_manager

        # Initialize the UI elements
        self.setup_ui()

        # Apply dark mode to the UI
        self.apply_dark_mode()

        # Force a resize after maximizing
        self.resize(self.width() - 1, self.height() - 1)
        self.resize(self.width() + 1, self.height() + 1)

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

    def resizeEvent(self, event):
        """Handle the resize event and delegate to the ResizeManager."""
        self.resize_manager.resize_main_window(self)
        super().resizeEvent(event)
