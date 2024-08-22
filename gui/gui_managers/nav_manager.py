# gui.gui_managers.nav_manager.py
class NavigationManager:
    def __init__(self, main_window):
        self.main_window = main_window


    def create_menus(self):
        """Skapa huvud applikationens menyer."""
        menu_bar = self.main_window.menuBar()

        # Skapa knapp för att navigera till Hem vyn
        self._create_home_menu(menu_bar)

        # Skapa knapp för att navigera till Uppdrags vyn
        self._create_task_menu(menu_bar)


    def _create_home_menu(self, menu_bar):
        """Skapa "Hem"-sidans meny"""
        home_menu = menu_bar.addMenu("Hem")
        home_menu.addAction("Hem", lambda: self.display_page("Hem"))


    def _create_task_menu(self, menu_bar):
        """Skapa uppdragssidans meny"""
        task_menu = menu_bar.addMenu("Uppdrag")
        task_menu.addAction("Skapa Uppdrag", lambda: self.display_page("Skapa Uppdrag"))
        task_menu.addAction("Visa Uppdrag", lambda: self.display_page("Uppdrag"))

    # Forcefully add and display
    def display_page(self, page_name):
        """Display the requested page by name."""
        print(f"Attempting to display page '{page_name}'")
        page = self.main_window.pages.get(page_name)
        if page:
            print(f"Page '{page_name}' exists. Widget: {page}")

            # Ensure the page is added to the stacked widget
            index = self.main_window.stacked_widget.indexOf(page)
            if index == -1:
                print(f"Page '{page_name}' not found in stacked widget. Adding it now.")
                self.main_window.stacked_widget.addWidget(page)
                index = self.main_window.stacked_widget.indexOf(page)

            # Display the page
            if index != -1:
                self.main_window.stacked_widget.setCurrentIndex(index)
                print(f"Page '{page_name}' displayed at index {index}.")
            else:
                print(f"Failed to find or add page '{page_name}' to stacked widget.")
        else:
            print(f"Page '{page_name}' not found. Please check if the page is correctly initialized.")


