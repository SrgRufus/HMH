# gui.gui_managers.nav_manager.py
from PyQt5.QtWidgets import QMenu # Importera nödvändiga widgets från PyQt5

class NavigationManager:
    def __init__(self, main_window, page_manager=None):
        """När vi skapar ett NavigationManager-objekt, sparar vi referenser till huvudfönstret och sidohanteraren."""
        self.main_window = main_window  # Huvudfönstret där menyerna kommer att visas
        self.page_manager = page_manager  # Sidohanteraren som används för att byta mellan sidor

    def create_menus(self):
        """Skapar huvudmenyerna för applikationen utan att skapa dubbletter."""
        menu_bar = self.main_window.menuBar()  # Hämtar menyraden från huvudfönstret
        menu_bar.clear()  # Rensar alla gamla menyer

        self._create_home_menu(menu_bar)  # Skapar "Hem"-menyn
        self._create_task_menu(menu_bar)  # Skapar "Uppdrag"-menyn
        self._create_placeholder_menus(menu_bar)  # Skapar platshållarmenyer

    def _create_home_menu(self, menu_bar):
        """Skapar 'Hem'-menyn och lägger till den i menyraden."""
        home_menu = QMenu("Hem", self.main_window)
        menu_bar.addMenu(home_menu)
        home_menu.addAction("Hem", lambda: self.page_manager.display_page("Hem"))  # Lägg till ett alternativ för att visa hemsidan

    def _create_task_menu(self, menu_bar):
        """Skapar 'Uppdrag'-menyn och lägger till den i menyraden."""
        task_menu = QMenu("Uppdrag", self.main_window)
        menu_bar.addMenu(task_menu)
        task_menu.addAction("Skapa Uppdrag", lambda: self.page_manager.display_page("Skapa Uppdrag"))  # Lägg till ett alternativ för att skapa en uppgift
        task_menu.addAction("Visa Uppdrag", lambda: self.page_manager.display_page("Uppdrag"))  # Lägg till ett alternativ för att visa uppgifter
        task_menu.addAction("Uppdatera Uppdrag", lambda: self.page_manager.display_page("Uppdatera Uppdrag"))  # Lägg till ett alternativ för att uppdatera en uppgift

    def open_update_task_page(self):
        """Opens the UpdateTaskPage directly without prompting for an ID."""
        self.main_window.page_manager.display_page("Uppdatera Uppdrag")

    def _create_placeholder_menus(self, menu_bar):
        """Skapar platshållarmenyer för 'Rapporter' och 'Inställningar'."""
        report_menu = QMenu("Rapporter", self.main_window)
        menu_bar.addMenu(report_menu)
        report_menu.addAction("Visa Rapport", lambda: self.page_manager.display_page("Visa Rapport"))  # Lägg till ett alternativ för att visa rapporter

        settings_menu = QMenu("Inställningar", self.main_window)
        menu_bar.addMenu(settings_menu)
        settings_menu.addAction("Allmänna Inställningar", lambda: self.page_manager.display_page("Inställningar"))  # Lägg till ett alternativ för att visa inställningar

    def display_page(self, page_name):
        """Ber sidohanteraren att visa en viss sida baserat på sidans namn."""
        self.page_manager.display_page(page_name)
