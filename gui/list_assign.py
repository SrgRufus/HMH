# gui.list_assign.py
from datetime import datetime, timedelta

from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel, QWidget, QMessageBox
)
from database.managers.assignment_manager import AssignmentManager
from gui.gui_managers.ui_elements.button_elements import CustomButtons
from gui.gui_managers.ui_elements.widgets import AssignmentTree


# Skapar ett ListAssign-widget.
class ListAssign(QWidget):
    def __init__(self, parent: QWidget, db_path: str, event_manager):
        super().__init__(parent)
        self.main_window = parent
        self.assignment_manager = AssignmentManager(db_path=db_path, event_manager=event_manager)
        self.event_manager = event_manager

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.title_label = QLabel("Uppdrag")
        layout.addWidget(self.title_label)

        self.assignment_tree = AssignmentTree()
        layout.addWidget(self.assignment_tree)

        button_grid = CustomButtons.create_button_grid([
            ("Hämta Uppdrag", self.populate_assignments),
            ("Öppna Uppdrag", self.open_assign),
            ("Uppdatera Status", self.update_status)
        ])
        layout.addLayout(button_grid)

        self.delete_button = CustomButtons.create_button("Ta bort uppdrag", self.delete_selected_assignment)
        layout.addWidget(self.delete_button)

        back_button = CustomButtons.create_button("Tillbaka till huvudmenyn", self.go_back)
        layout.addWidget(back_button)

        self.populate_assignments()

    def go_back(self):
        """
        Navigerar tillbaka till huvudmenyn.
        """
        self.main_window.display_page("Hem")

    def populate_assignments(self):
        try:
            current_date = datetime.now().date()
            start_of_week = current_date - timedelta(days=current_date.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            assignments = self.assignment_manager.fetcher.fetch_assignments_for_current_week(start_of_week, end_of_week)
            sorted_assignments = self.assignment_manager.sort_assignments(assignments)
            today_date_str = current_date.strftime('%Y-%m-%d')

            self.assignment_tree.clear_tree()

            for assignment in sorted_assignments:
                self.assignment_tree.add_assignment(assignment, today_date_str)
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_selected_assignment(self):
        selected_item = self.assignment_tree.currentItem()
        if selected_item:
            reply = QMessageBox.question(
                self, "Bekräfta borttagning",
                f"Är du säker på att du vill ta bort uppdraget '{selected_item.text(1)}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    assignment_id = int(selected_item.text(0))
                    self.assignment_manager.delete_assignment(assignment_id)
                    self.assignment_tree.takeTopLevelItem(self.assignment_tree.indexOfTopLevelItem(selected_item))
                except RuntimeError as e:
                    QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Inget uppdrag valt", "Välj ett uppdrag att ta bort.")

    def open_assign(self):
        selected_item = self.assignment_tree.currentItem()
        if selected_item:
            try:
                assignment_id = int(selected_item.text(0))
                assignment = self.assignment_manager.fetch_assignment_by_id(assignment_id)
                QMessageBox.information(self, "Öppna Uppdrag", f"Uppdrag: {assignment.kommun}, {assignment.adress}")
            except RuntimeError as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Inget uppdrag valt", "Välj ett uppdrag att öppna.")

    def update_status(self):
        selected_item = self.assignment_tree.currentItem()
        if selected_item:
            try:
                assignment_id = int(selected_item.text(0))
                self.assignment_manager.update_job_status(assignment_id, 'Completed')
                QMessageBox.information(self, "Uppdatera Status", "Statusen för uppdraget har uppdaterats till 'Completed'.")
                self.populate_assignments()
            except RuntimeError as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Inget uppdrag valt", "Välj ett uppdrag att uppdatera statusen för.")

