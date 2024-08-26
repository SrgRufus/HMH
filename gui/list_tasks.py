# gui/list_tasks.py
import logging
from datetime import datetime

from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QMessageBox

from database import TaskManager
from gui.resize_manager import ResizeManager
from gui.ui_elements.button_elements import CustomButtons
from gui.ui_elements.widgets import TaskTree


class ListTasks(QWidget):

    def __init__(self, parent: QWidget, session, event_manager):
        """Konstruktor för att initiera ListTasks med referenser till huvudfönstret, sessionen och event manager."""
        super().__init__(parent)
        self.main_window = parent  # Referens till huvudfönstret
        self.session = session  # Lagrar sessionen som ett attribut
        self.event_manager = event_manager  # Lagrar event manager för hantering av händelser
        self.task_manager = TaskManager(self.session)  # Instansierar TaskManager med sessionen

        self.resize_manager = ResizeManager()  # Initierar ResizeManager för att hantera storleksändring

        # Initierar attribut för UI-komponenter
        self.title_label = QLabel("Uppdrag")
        self.task_tree = TaskTree()  # En anpassad widget för att visa uppgifter
        self.delete_button = None  # Kommer att initialiseras i `init_ui`

        self.init_ui()  # Initierar användargränssnittet

    def init_ui(self):
        """Initierar användargränssnittet och layouten för sidan."""
        layout = QVBoxLayout(self)
        self.title_label = QLabel("Uppdrag")
        layout.addWidget(self.title_label)

        self.task_tree = TaskTree()
        layout.addWidget(self.task_tree)

        # Lägg till knappar för att växla mellan aktiva och slutförda uppdrag
        button_grid = CustomButtons.create_button_grid([
            ("Visa Aktiva Uppdrag", self.populate_active_tasks),
            ("Visa Slutförda Uppdrag", self.populate_completed_tasks),
            ("Uppdatera Status", self.update_status),
            ("Ta bort uppdrag", self.delete_selected_task)
        ])
        layout.addLayout(button_grid)

        # Backknapp för navigering
        back_button = CustomButtons.create_button("Backa", self.go_back)
        layout.addWidget(back_button)

        # Ladda aktiva uppdrag som standard
        self.populate_active_tasks()

    def go_back(self):
        """Gå tillbaka till hemsidan."""
        self.main_window.display_page("Hem")

    def populate_active_tasks(self):
        """Hämtar och visar aktiva uppdrag."""
        try:
            tasks = self.task_manager.get_tasks_by_status('Aktiv')
            logging.info(f"Retrieved {len(tasks)} active tasks")

            sorted_tasks = self.task_manager.sort_tasks(tasks)
            today_date_str = datetime.now().strftime('%Y-%m-%d')

            self.task_tree.clear_tree()  # Rensa trädet innan det fylls på nytt

            for task in sorted_tasks:
                logging.info(f"Adding active task: {task.kommun}, {task.adress}, {task.next_occurrence_date}")
                self.task_tree.add_task(task, today_date_str)  # Lägg till uppgift i trädet
        except Exception as e:
            logging.exception("Error while populating active tasks")
            QMessageBox.critical(self, "Error", str(e))

    def populate_completed_tasks(self):
        """Hämtar och visar slutförda uppdrag."""
        try:
            tasks = self.task_manager.get_tasks_by_status('Completed')
            logging.info(f"Retrieved {len(tasks)} completed tasks")

            sorted_tasks = self.task_manager.sort_tasks(tasks)
            today_date_str = datetime.now().strftime('%Y-%m-%d')

            self.task_tree.clear_tree()

            for task in sorted_tasks:
                logging.info(f"Adding completed task: {task.kommun}, {task.adress}, {task.next_occurrence_date}")
                self.task_tree.add_task(task, today_date_str)
        except Exception as e:
            logging.exception("Error while populating completed tasks")
            QMessageBox.critical(self, "Error", str(e))

    def delete_selected_task(self):
        """Tar bort den valda uppgiften."""
        selected_item = self.task_tree.currentItem()
        if selected_item:
            reply = QMessageBox.question(
                self, "Bekräfta borttagning",
                f"Är du säker på att du vill ta bort uppdraget '{selected_item.text(1)}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    task_id = int(selected_item.text(0))  # Extrahera task_id från det valda objektet
                    self.task_manager.delete_task(task_id)  # Ta bort uppgiften
                    self.task_tree.takeTopLevelItem(self.task_tree.indexOfTopLevelItem(selected_item))  # Ta bort objektet från trädet
                    logging.info(f"Task ID {task_id} deleted successfully.")
                    self.populate_tasks()  # Uppdatera listan över uppgifter
                except Exception as e:
                    logging.exception("Error deleting task")
                    QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Inget uppdrag valt", "Välj ett uppdrag att ta bort.")

    def open_task(self):
        """Öppnar detaljer för den valda uppgiften."""
        selected_item = self.task_tree.currentItem()
        if selected_item:
            try:
                task_id = int(selected_item.text(0))  # Extrahera task_id från det valda objektet
                task = self.task_manager.fetch_task_by_id(task_id)
                if task:
                    QMessageBox.information(self, "Öppna Uppdrag", f"Uppdrag: {task.kommun}, {task.adress}")
                else:
                    logging.warning(f"Task with ID {task_id} not found")
                    QMessageBox.warning(self, "Error", "Task not found.")
            except Exception as e:
                logging.exception("Error while opening task")
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Inget uppdrag valt", "Välj ett uppdrag att öppna.")

    def update_status(self):
        """Uppdaterar statusen för den valda uppgiften."""
        selected_item = self.task_tree.currentItem()
        if selected_item:
            try:
                task_id = int(selected_item.text(0))
                task = self.task_manager.fetch_task_by_id(task_id)
                if not task:
                    logging.warning(f"Task with ID {task_id} not found")
                    QMessageBox.warning(self, "Task not found", "The selected task does not exist.")
                    return

                logging.info(f"Completing task ID: {task_id} and creating new one")
                new_task = self.task_manager.complete_task_and_create_new(task_id)
                if new_task:
                    QMessageBox.information(self, "Uppdatera Status",
                                            "Order has been completed, and a new one has been created.")
                    self.populate_tasks()  # Uppdatera listan över uppgifter
                else:
                    QMessageBox.critical(self, "Error", "Failed to complete the order and create a new one.")
            except Exception as e:
                logging.exception("Error completing task and creating new one")
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Inget uppdrag valt", "Välj ett uppdrag att uppdatera statusen för.")

    def resizeEvent(self, event):
        """Hantera resize-händelse och delegera till ResizeManager."""
        self.resize_manager.resize_list_tasks(self)
        super().resizeEvent(event)
