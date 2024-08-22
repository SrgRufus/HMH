# gui.mainwindow.py : Improved UI setup and modularization
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QStackedWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from gui.gui_managers.nav_manager import NavigationManager
from gui.gui_managers.page_manager import PageManager
from gui.gui_managers.ui_elements.button_elements import CustomButtons
from gui.gui_managers.ui_elements.search_bar import SearchBar
from database.managers.task_manager import TaskManager
from database.managers.event_manager import EventManager
from database.managers.recurrence_manager import RecurrenceManager
from database.connection import Session as DBSession



class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.session = DBSession() # Initialize DB session
        self.recurrence_manager = RecurrenceManager() # Pass session to RecurrenceManager
        self.event_manager = EventManager(self.recurrence_manager) # Pass RecurrenceManager to EventManager
        self.task_manager = TaskManager()

        self.page_manager = PageManager(self)
        self.pages = self.page_manager.create_pages()

        print("Pages initialized", self.pages)
        # self.pages = {}

        self.stacked_widget = QStackedWidget()
        self.navigation_manager = NavigationManager(self)
        self.setup_ui()
        self.setWindowTitle("HMH: Henry's Molok Hanterare")
        self.setGeometry(100, 100, 1200, 800)
        self.apply_dark_mode()

    def setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Lägg till en logotyp i framtiden
        # Se till att logotypen ligger i "assets" mappen i root

        logo_label = QLabel(self)
        pixmap = QPixmap("assets/remondis-logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)


        layout.addWidget(self.stacked_widget)
        # self._populate_stacked_widget()

        # Infoga navigeringsmenyer
        # Directly add and display the 'Hem' page
        home_page = self.page_manager.create_home_page()
        self.stacked_widget.addWidget(home_page)
        index = self.stacked_widget.indexOf(home_page)
        print(f"'Hem' page added at index {index}.")  # Debugging info

        # Attempt to display the 'Hem' page directly
        self.stacked_widget.setCurrentIndex(index)
        print(f"Displaying 'Hem' page directly.")

        self.navigation_manager.create_menus()

        # self.navigation_manager.display_page("Hem")

    def _populate_stacked_widget(self) -> None:
        for page_name, page_widget in self.pages.items():
            print(f"Adding page {page_name} to stacked widget.")  # Debug print
            self.stacked_widget.addWidget(page_widget)
            widget_index = self.stacked_widget.indexOf(page_widget)
            print(f"Page '{page_name}' added at index {widget_index}.")  # Confirm the index


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
            QPushButton {{
                background-color: {dark_palette["background-color"]};
                border: 1px solid {dark_palette["border-color"]};
                border-radius: 5px;
                padding: 5px;
                color: {dark_palette["color"]};
            }}
            QPushButton:hover {{
                background-color: #3a3a3a;
                border: 1px solid #0078d7;
            }}
            """
        )


    def _initialize_ui_elements(self, layout: QVBoxLayout) -> None:
        self.search_bar = SearchBar(self)
        layout.addLayout(self.search_bar)
        layout.addWidget(self.search_bar.search_result_label)
        self.custom_buttons = CustomButtons(self.navigation_manager)
        layout.addLayout(self.custom_buttons)