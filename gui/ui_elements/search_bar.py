# gui.ui_elements.search_bar.py : Enhanced for extensibility
from PyQt5.QtWidgets import QLineEdit

class SearchBar(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Sök...")
        self.textChanged.connect(self.filter_tasks)

    @staticmethod
    def filter_tasks(text):
        """Implementera söklogik här, efter jag har sökt reda på hur fan man gör det."""
        print(f"Filtering tasks based on input: {text}")
        # Placeholder for search/filter logic
        # Example: self.parent().task_manager.filter_tasks(text)
        pass


