# gui.ui_elements.button_elements.py
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import QSize


class CustomButtons(QVBoxLayout):
    def __init__(self, navigation_manager, parent=None):
        super().__init__(parent)

        button_texts = ["Uppdrag", "Skapa uppdrag", "Sök uppdrag", "Inställningar", "Historik", "Statistik"]
        for text in button_texts:
            button = self.create_button(text, lambda checked, page_name=text: navigation_manager.display_page(page_name))
            self.addWidget(button)

    # Skapar en knapp och kopplar den till en funktion.
    @staticmethod
    def create_button(label: str, callback) -> QPushButton:
        """
        :param label: Knappens etikett.
        :param callback: Funktion att anropa när knappen trycks.
        :return: En QPushButton-instans.
        """
        button = QPushButton(label)
        button.clicked.connect(callback)
        return button

    # Skapar ett rutnät med knappar för olika handlingar.
    @staticmethod
    def create_button_grid(actions: list) -> QGridLayout:
        """
        :return: QGridLayout som innehåller knapparna.
        """
        grid_layout = QGridLayout()
        button_size = QSize(150, 50)

        for i, (label, action) in enumerate(actions):
            button = CustomButtons.create_button(label, action)
            button.setFixedSize(button_size)
            grid_layout.addWidget(button, 0, i)

        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(10)

        return grid_layout
