# gui.ui_elements.widgets.py : TaskTree Widget with custom styling
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QColor, QBrush, QFont
from PyQt5.QtCore import Qt
from datetime import datetime

class TaskTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(11)
        self.setHeaderLabels([
            "ID", "Kommun", "Adress", "Ort", "Material",
            "Tömningsfrekvens", "Nästa Tömningsdatum", "Status",
            "Info", "Förare", "Koordinater"
        ])
        self.setStyleSheet(
            """
            QTreeWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border: none;
                font-size: 14px;
            }
            QTreeWidget::item {
                border: 1px solid #3a3a3a;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
                background-color: #3c3c3c;
            }
            QTreeWidget::item:selected {
                background-color: #0078d7;
                color: #ffffff;
            }
            """
        )

    def add_task(self, task, today_date_str):
        """Add a task to the tree with a card-like appearance."""
        if isinstance(task.next_occurrence_date, str):
            try:
                task.next_occurrence_date = datetime.strptime(task.next_occurrence_date, '%Y-%m-%d')
            except ValueError:
                task.next_occurrence_date = None

        next_date_str = task.next_occurrence_date.strftime('%Y-%m-%d') if task.next_occurrence_date else ""
        date_indicator = "IDAG" if next_date_str == today_date_str else next_date_str

        item = QTreeWidgetItem([
            str(task.id), task.kommun, task.adress, task.ort,
            task.material, task.tomningsfrekvens, date_indicator,
            task.status, task.info or "",
                         task.chauffor or "", task.koordinater or ""
        ])

        item.setFont(0, QFont("Arial", 12, QFont.Bold))
        item.setTextAlignment(0, Qt.AlignCenter)
        self._apply_date_coloring(item, next_date_str, today_date_str)
        self.addTopLevelItem(item)

    @staticmethod
    def _apply_date_coloring(item, next_date_str, today_date_str):
        """Applicera bakgrundsfärg baserat på datums relevans (idag = gul, försenad/igår = röd)"""
        if next_date_str == today_date_str:
            item.setBackground(6, QBrush(QColor('yellow')))
        elif next_date_str < today_date_str:
            item.setBackground(6, QBrush(QColor('red')))

    def clear_tree(self):
        """Rensa alla objekt från trädet"""
        self.clear()
