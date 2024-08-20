# gui.gui_managers.nav_manager.py
from PyQt5.QtWidgets import QMenu, QMenuBar


class NavigationManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_bar = QMenuBar(main_window)
        self.pages = main_window.pages

    def create_menus(self):
        # Skapa menyraden och dess menyer
        file_menu = QMenu("&File", self.main_window)
        view_menu = QMenu("&View", self.main_window)
        help_menu = QMenu("&Help", self.main_window)

        # Lägg till menyalternativ för File-menyn
        file_menu.addAction("Open", self.open_file)
        file_menu.addAction("Exit", self.main_window.close)

        # Lägg till menyalternativ för View-menyn
        view_menu.addAction("Home", lambda: self.display_page("Hem"))
        view_menu.addAction("Tasks", lambda: self.display_page("Uppdrag"))
        view_menu.addAction("Create Task", lambda: self.display_page("Skapa Uppdrag"))

        # Lägg till menyalternativ för Help-menyn
        help_menu.addAction("About", self.show_about_dialog)

        # Lägg till menyerna till menyraden
        self.menu_bar.addMenu(file_menu)
        self.menu_bar.addMenu(view_menu)
        self.menu_bar.addMenu(help_menu)

        # Sätt menyraden i huvudfönstret
        self.main_window.setMenuBar(self.menu_bar)

    def display_page(self, page_name):
        # Visa den valda sidan med felhantering
        try:
            page = self.pages[page_name]
            self.main_window.stacked_widget.setCurrentWidget(page)
        except KeyError:
            print(f"Sidan {page_name} finns inte.")

    def open_file(self):
        # Platshållare: Öppna Fil, logik för att öppna en fil
        print("Open file dialog")

    def show_about_dialog(self):
        # Logik för att visa en dialogruta med information om applikationen
        print("Show about dialog")
