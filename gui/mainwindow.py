# gui.mainwindow.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget, QVBoxLayout

from gui.gui_managers.nav_manager import NavigationManager
from gui.gui_managers.page_manager import PageManager
from gui.gui_managers.ui_elements.button_elements import CustomButtons
from gui.gui_managers.ui_elements.search_bar import SearchBar

class MainWindow(QMainWindow):
    def __init__(self, db_path: str, event_manager, task_manager) -> None:
        super().__init__()
        self.db_path = db_path
        self.event_manager = event_manager
        self.task_manager = task_manager
        self.page_manager = PageManager(self)  # Initiera PageManager

        # Definiera attribut i __init__
        self.pages = {}  # Initiera self.pages
        self.stacked_widget = QStackedWidget()  # Initiera self.stacked_widget

        # Skapa sidorna med PageManager
        self.pages = self.page_manager.create_pages()  # Använd den definierade self.pages

        # Nu kan vi initiera NavigationManager eftersom self.pages nu är definierat
        self.navigation_manager = NavigationManager(self)

        self.setup_ui()
        self.setWindowTitle("HMH: Henry's Molok Hanterare")
        self.setGeometry(100, 100, 800, 600)

    def setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.stacked_widget)

        self._populate_stacked_widget()

        # Låt NavigationManager hantera meny och första sida
        self.navigation_manager.create_menus()
        self.navigation_manager.display_page("Hem")

    def _populate_stacked_widget(self) -> None:
        for page_name, page_widget in self.pages.items():
            self.stacked_widget.addWidget(page_widget)

    def _initialize_ui_elements(self, layout: QVBoxLayout) -> None:
        self.search_bar = SearchBar(self)

        layout.addLayout(self.search_bar)
        layout.addWidget(self.search_bar.search_result_label)

        self.custom_buttons = CustomButtons(self.navigation_manager)
        layout.addLayout(self.custom_buttons)