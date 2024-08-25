# gui.ui_elements.button_elements.py : Customized buttons with hover effects
from PyQt5.QtWidgets import QPushButton, QGridLayout
from PyQt5.QtCore import QSize, Qt

class CustomButtons(QGridLayout):
    def __init__(self, navigation_manager, parent=None):
        super().__init__(parent)
        button_texts = (
            ["Uppdrag", "Skapa Uppdrag", "Sök uppdrag",
             "Inställningar", "Historik", "Statistik"]
        )
        # Define the number of columns you want in the grid
        columns = 3

        for i, text in enumerate(button_texts):
            button = self.create_button(text,
                                        lambda checked, page_name=text: navigation_manager.display_page(page_name))
            row = i // columns
            col = i % columns
            self.addWidget(button, row, col)

    @staticmethod
    def create_button(label: str, callback) -> QPushButton:
        """Create a QPushButton with custom styling."""
        button = QPushButton(label)
        button.setFixedSize(QSize(200, 40))
        button.clicked.connect(callback)

        button.setStyleSheet(
            """
            QPushButton {
                background-color: #8B0000;  /* Dark red color */
                color: #ffffff;
                border-radius: 10px;
                border: none;
                padding: 10px;
                font-size: 16px;  /* Increased font size */
                font-weight: bold;  /* Bold font */
            }
            QPushButton:hover {
                background-color: #600000;  /* Slightly darker red on hover */
            }
            QPushButton:pressed {
                background-color: #4B0000;  /* Even darker red when pressed */
            }
            """
        )
        return button

    @staticmethod
    def create_button_grid(actions: list, columns: int = 3,
                           h_spacing: int = 10, v_spacing: int = 10,
                           margins: tuple = (1000, 10, 10, 10),
                           alignment: Qt.AlignmentFlag = Qt.AlignCenter) -> QGridLayout:
        """Create a grid of buttons with customizable layout options."""
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(h_spacing)
        grid_layout.setVerticalSpacing(v_spacing)
        grid_layout.setContentsMargins(*margins)

        for i, (label, callback) in enumerate(actions):  # Removed *button_args
            button = CustomButtons.create_button(label, callback)
            row = i // columns
            col = i % columns
            grid_layout.addWidget(button, row, col, alignment)

        return grid_layout
