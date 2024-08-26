# gui/mainwindow.py
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QStackedWidget

from database import EventManager, RecurrenceManager, TaskManager, Session as DBSession
from .gui_managers import NavigationManager, PageManager
from .ui_elements import CustomButtons, SearchBar
from .resize_manager import ResizeManager

class MainWindow(QMainWindow):
    def __init__(self, session):
        """Konstruktor för huvudfönstret där alla komponenter sätts upp."""
        super(MainWindow, self).__init__()
        self.session = session
        self.task_manager = TaskManager(session)
        self.setWindowTitle("HMH: Henry's Molok Hanterare")
        self.setGeometry(100, 100, 1200, 800)  # Sätter standardstorleken för huvudfönstret

        self.resize_manager = ResizeManager()  # Initierar ResizeManager för att hantera storleksändring

        # Initiera nödvändiga hanterare
        self.session = DBSession()
        self.recurrence_manager = RecurrenceManager()
        self.event_manager = EventManager(self.recurrence_manager)
        self.task_manager = TaskManager(session)

        # Sätt upp den staplade widgeten som används för att byta mellan olika sidor
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initiera NavigationManager först med en platshållare för page_manager
        self.navigation_manager = NavigationManager(self, page_manager=None)

        # Initiera PageManager med bara huvudfönstret
        self.page_manager = PageManager(self, self.session)

        # Uppdatera nu NavigationManager med den verkliga PageManager
        self.navigation_manager.page_manager = self.page_manager

        # Initiera UI-elementen
        self.setup_ui()

        # Applicera dark mode till UI:t
        self.apply_dark_mode()

        # Tvinga en storleksändring efter maximering
        self.resize(self.width() - 1, self.height() - 1)
        self.resize(self.width() + 1, self.height() + 1)

    def show_update_task_page(self, task_id):
        """Öppnar uppdateringssidan för uppgifter för det angivna uppgifts-ID:t."""
        update_page = self.page_manager.pages["Uppdatera Uppdrag"]
        update_page.load_task_details(task_id)  # Laddar uppgiftsdetaljer baserat på ID
        self.page_manager.display_page("Uppdatera Uppdrag")

    def setup_ui(self) -> None:
        """Skapar och lägger till UI-element till huvudfönstret."""
        # Skapa startsidan och lägg till den till den staplade widgeten
        home_page = self.page_manager.create_home_page()
        self.stacked_widget.addWidget(home_page)

        # Visa startsidan initialt
        self.page_manager.display_page("Hem")

        # Lägg till logotypen på startsidan
        logo_label = QLabel()
        pixmap = QPixmap("assets/remondis-logo.png")  # Anta att bilden finns i "assets"-mappen
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Lägg till logotypen i layouten på startsidan
        home_layout = self.stacked_widget.widget(self.stacked_widget.indexOf(home_page)).layout()
        home_layout.addWidget(logo_label)

        # Skapa navigationsmenyer
        self.navigation_manager.create_menus()

    def apply_dark_mode(self):
        """Applicerar ett mörkt tema på hela applikationen."""
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
        )  # Ställer in stilen för hela applikationen

    def _initialize_ui_elements(self, layout: QVBoxLayout) -> None:
        """Initierar UI-element som sökfält och anpassade knappar."""
        self.search_bar = SearchBar(self)  # Instansierar ett sökfält
        layout.addLayout(self.search_bar)  # Lägg till sökfältet i layouten
        layout.addWidget(self.search_bar.search_result_label)  # Lägg till sökresultat etiketten i layouten
        self.custom_buttons = CustomButtons(self.navigation_manager)  # Instansierar anpassade knappar
        layout.addLayout(self.custom_buttons)  # Lägg till knapparna i layouten

    def resizeEvent(self, event):
        """Hantera storleksändringshändelsen och delegera till ResizeManager."""
        self.resize_manager.resize_main_window(self)
        super().resizeEvent(event)
