# gui.gui_managers.ui_elements.widgets.py
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QColor, QBrush
from datetime import datetime

class AssignmentTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(11)
        self.setHeaderLabels([
            "ID",
            "Kommun",
            "Adress",
            "Ort",
            "Material",
            "Tömningsfrekvens",
            "Nästa Tömningsdatum",
            "Status",
            "Info",
            "Förare",
            "Koordinater"
        ])

    def add_assignment(self, assignment, today_date_str):
        """
        Lägger till ett uppdrag i trädet och markerar efter status och datum.
        """
        # Säkerställ att next_occurrence_date är ett datetime-objekt
        if isinstance(assignment.next_occurrence_date, str):
            try:
                assignment.next_occurrence_date = datetime.strptime(assignment.next_occurrence_date, '%Y-%m-%d')
            except ValueError:
                assignment.next_occurrence_date = None

        next_date_str = assignment.next_occurrence_date.strftime('%Y-%m-%d') if assignment.next_occurrence_date else ""
        date_indicator = "IDAG" if next_date_str == today_date_str else next_date_str

        item = QTreeWidgetItem([
            str(assignment.id),
            assignment.kommun,
            assignment.adress,
            assignment.ort,
            assignment.material,
            assignment.tomningsfrekvens,
            date_indicator,
            assignment.status,
            assignment.info if assignment.info else "",
            assignment.chauffor if assignment.chauffor else "",
            assignment.koordinater if assignment.koordinater else ""
        ])

        # Färga baserat på datum
        if next_date_str == today_date_str:
            item.setBackground(6, QBrush(QColor('yellow')))  # Markera "Nästa Tömningsdatum"-kolumnen
        elif next_date_str < today_date_str:
            item.setBackground(6, QBrush(QColor('red')))  # Försenade uppdrag markeras i rött

        self.addTopLevelItem(item)

    def clear_tree(self):
        """
        Rensar trädet från alla poster.
        """
        self.clear()
