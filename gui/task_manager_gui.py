# gui/task_manager_gui.py
from PyQt5.QtWidgets import QWidget, QMessageBox
from database.managers.task_manager import TaskManager

class TaskManagerGUI(QWidget):
    def __init__(self, session):
        super().__init__()
        self.task_manager = TaskManager(session)

    def complete_task(self, task_id: int):
        """Hanterar slutförandet av ett uppdrag och skapar ett nytt."""
        result = self.task_manager.mark_task_as_completed(task_id)
        if result:
            QMessageBox.information(self, "Framgång", "Uppdraget har markerats som slutfört och ett nytt uppdrag har skapats.")
        else:
            QMessageBox.critical(self, "Fel", "Ett fel uppstod vid slutförandet av uppdraget.")
