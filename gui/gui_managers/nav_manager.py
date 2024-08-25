# gui.gui_managers.nav_manager.py
from PyQt5.QtWidgets import QMenu


class NavigationManager:
    def __init__(self, main_window, page_manager=None):
        self.main_window = main_window
        self.page_manager = page_manager

    def create_menus(self):
        """Create the main application's menus without duplicates."""
        menu_bar = self.main_window.menuBar()
        menu_bar.clear()

        self._create_home_menu(menu_bar)
        self._create_task_menu(menu_bar)
        self._create_placeholder_menus(menu_bar)

    def _create_home_menu(self, menu_bar):
        home_menu = QMenu("Hem", self.main_window)
        menu_bar.addMenu(home_menu)
        home_menu.addAction("Hem", lambda: self.page_manager.display_page("Hem"))

    def _create_task_menu(self, menu_bar):
        task_menu = QMenu("Uppdrag", self.main_window)
        menu_bar.addMenu(task_menu)
        task_menu.addAction("Skapa Uppdrag", lambda: self.page_manager.display_page("Skapa Uppdrag"))
        task_menu.addAction("Visa Uppdrag", lambda: self.page_manager.display_page("Uppdrag"))

    def _create_placeholder_menus(self, menu_bar):
        report_menu = QMenu("Rapporter", self.main_window)
        menu_bar.addMenu(report_menu)
        report_menu.addAction("Visa Rapport", lambda: self.page_manager.display_page("Visa Rapport"))

        settings_menu = QMenu("Inställningar", self.main_window)
        menu_bar.addMenu(settings_menu)
        settings_menu.addAction("Allmänna Inställningar", lambda: self.page_manager.display_page("Inställningar"))

    def display_page(self, page_name):
        """Delegate page display to PageManager."""
        self.page_manager.display_page(page_name)
