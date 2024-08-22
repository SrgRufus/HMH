# gui.list_tasks.py : Enhanced version with improved task interaction and error handling
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QMessageBox
from gui.gui_managers.ui_elements.button_elements import CustomButtons
from gui.gui_managers.ui_elements.widgets import TaskTree
from database.managers.task_manager import TaskManager


class ListTasks(QWidget):
    def __init__(self, parent: QWidget, event_manager):
        super().__init__(parent)
        self.main_window = parent
        self.task_manager = TaskManager()
        self.event_manager = event_manager


        # Initialize attributes
        self.title_label = QLabel("Uppdrag")
        self.task_tree = TaskTree()
        self.delete_button = None  # Will be initialized in `init_ui`

        self.init_ui()



    def init_ui(self):
        layout = QVBoxLayout(self)
        self.title_label = QLabel("Uppdrag")
        layout.addWidget(self.title_label)

        self.task_tree = TaskTree()
        layout.addWidget(self.task_tree)

        # Button grid for task actions
        button_grid = CustomButtons.create_button_grid([
            ("Hämta Uppdrag", self.populate_tasks), ("Öppna Uppdrag", self.open_task), ("Uppdatera Status", self.update_status),
            ("Ta bort uppdrag", self.delete_selected_task)
        ])
        layout.addLayout(button_grid)

        # "Delete" knapp
       # self.delete_button = CustomButtons.create_button [klistra in delete knappen här om det skulle behövas]
       # layout.addWidget(self.delete_button)

        # Tillbaka knapp för att navigera tillbaka till startsidan
        back_button = CustomButtons.create_button("Backa", self.go_back)
        layout.addWidget(back_button)

        self.populate_tasks()


    def go_back(self):
        self.main_window.display_page("Hem")


    def populate_tasks(self):
        try:
            current_date = datetime.now().date()
            start_of_week = current_date - timedelta(days=current_date.weekday())

            tasks = self.task_manager.get_tasks_for_date(start_of_week)
            sorted_tasks = self.task_manager.sort_tasks(tasks)
            today_date_str = current_date.strftime('%Y-%m-%d')

            self.task_tree.clear_tree()

            for task in sorted_tasks:
                self.task_tree.add_task(task, today_date_str)
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))


    def delete_selected_task(self):
        selected_item = self.task_tree.currentItem()
        if selected_item:
            reply = QMessageBox.question(
                self, "Bekräfta borttagning",
                f"Är du säker på att du vill ta bort uppdraget '{selected_item.text(1)}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    task_id = int(selected_item.text(0))
                    self.task_manager.delete_task(task_id)
                    self.task_tree.takeTopLevelItem(self.task_tree.indexOfTopLevelItem(selected_item))
                except RuntimeError as e:
                    QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Inget uppdrag valt", "Välj ett uppdrag att ta bort.")


    def open_task(self):
        selected_item = self.task_tree.currentItem()
        if selected_item:
            try:
                task_id = int(selected_item.text(0))
                task = self.task_manager.fetch_task_by_id(task_id)  # Now this method is available again
                if task:
                    QMessageBox.information(self, "Öppna Uppdrag", f"Uppdrag: {task.kommun}, {task.adress}")
                else:
                    QMessageBox.warning(self, "Error", "Task not found.")
            except RuntimeError as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Inget uppdrag valt", "Välj ett uppdrag att öppna.")


    def update_status(self):
        selected_item = self.task_tree.currentItem()
        if selected_item:
            try:
                task_id = int(selected_item.text(0))
                self.task_manager.update_task_status(task_id, 'Completed')
                QMessageBox.information(self, "Uppdatera Status", "Statusen för uppdraget har uppdaterats till 'Completed'.")
                self.populate_tasks()
            except RuntimeError as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Inget uppdrag valt", "Välj ett uppdrag att uppdatera statusen för.")
