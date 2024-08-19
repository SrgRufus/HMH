# gui.ui_elements.search_bar.py
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox


class SearchBar(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Sök på Ort, Kommun, eller material")
        self.search_input.returnPressed.connect(self.perform_search)

        search_button = QPushButton("Sök")
        search_button.clicked.connect(self.perform_search)

        self.addWidget(self.search_input)
        self.addWidget(search_button)

        self.search_result_label = QLabel("")

    def perform_search(self):
        search_query = self.search_input.text().strip()
        if search_query:
            self.search_result_label.setText(f"Söker efter: {search_query}")
            # Här kan du integrera den faktiska söklogiken och visa resultat
        else:
            QMessageBox.warning(self.parent(), "Söksträng saknas", "Ange ett giltigt sökvärde.")
