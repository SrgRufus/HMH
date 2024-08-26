# gui/update_task_page.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTreeWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QDialog, QGridLayout, QTreeWidgetItem, QInputDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

from controllers.task_controller import TaskController  # Ensure this import path is correct

class UpdateTaskPage(QWidget):
    def __init__(self, parent, session):
        super().__init__(parent)
        self.session = session
        self.task_controller = TaskController(session)

        self.filter_input = QLineEdit()
        self.task_tree = QTreeWidget()
        self.task_tree.setColumnCount(6)
        self.task_tree.setHeaderLabels(["ID", "Kommun", "Adress", "Ort", "Status", "Nästa händelse"])
        self.task_tree.itemDoubleClicked.connect(self.open_task_dialog)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Filter Layout
        filter_layout = QHBoxLayout()
        self.filter_input.setPlaceholderText("Filtrera på ID, Kommun, Adress...")
        self.filter_input.textChanged.connect(self.filter_tasks)
        filter_layout.addWidget(QLabel("Filtrera:"))
        filter_layout.addWidget(self.filter_input)
        layout.addLayout(filter_layout)

        # Task Tree
        layout.addWidget(self.task_tree)

        # Load Tasks
        self.load_tasks()

    def load_tasks(self):
        tasks = self.task_controller.fetch_all_tasks()
        # Removed the incorrect setRowCount method

        for task in tasks:
            item = QTreeWidgetItem([
                str(task.id),
                task.kommun,
                task.adress,
                task.ort,
                task.status,
                task.next_occurrence_date.strftime('%Y-%m-%d') if task.next_occurrence_date else ''
            ])
            self.task_tree.addTopLevelItem(item)

    def filter_tasks(self, text):
        # Iterate through all top-level items and hide those that don't match the filter
        for i in range(self.task_tree.topLevelItemCount()):
            item = self.task_tree.topLevelItem(i)
            # Check if the filter text is in any of the relevant columns
            match = (
                text.lower() in item.text(0).lower() or
                text.lower() in item.text(1).lower() or
                text.lower() in item.text(2).lower()
            )
            item.setHidden(not match)

    def open_task_dialog(self, item):
        try:
            task_id = int(item.text(0))
        except ValueError:
            # Handle the case where ID is not an integer
            return

        task = self.task_controller.fetch_task_by_id(task_id)
        if task:
            dialog = TaskEditDialog(self, task, self.task_controller)
            if dialog.exec_() == QDialog.Accepted:
                # Optionally, refresh the task list to reflect changes
                self.load_tasks()

class TaskEditDialog(QDialog):
    def __init__(self, parent, task, task_controller):
        super().__init__(parent)
        self.task = task
        self.task_controller = task_controller
        self.setWindowTitle(f"Edit Task - {task.id}")
        self.setMinimumSize(400, 300)

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        fields = [
            ('Kommun', self.task.kommun),
            ('Adress', self.task.adress),
            ('Ort', self.task.ort),
            ('Material', self.task.material),
            ('Tömningsfrekvens', self.task.tomningsfrekvens),
            ('Status', self.task.status),
            ('Info', self.task.info),
            ('Chaufför', self.task.chauffor),
            ('Koordinater', self.task.koordinater),
        ]

        self.field_labels = {}  # To keep references to labels for updating

        for i, (label, value) in enumerate(fields):
            lbl = QLabel(label)
            field = QLabel(value)
            self.field_labels[label] = field
            edit_button = QPushButton()
            edit_button.setIcon(QIcon("path/to/edit_icon.png"))  # Ensure the icon path is correct
            edit_button.setIconSize(QSize(16, 16))
            # Fix the lambda to avoid shadowing by renaming the parameters
            edit_button.clicked.connect(lambda checked, f=field, l=label: self.edit_field(f, l))

            layout.addWidget(lbl, i, 0)
            layout.addWidget(field, i, 1)
            layout.addWidget(edit_button, i, 2)

            # Add Save and Cancel buttons
            save_button = QPushButton("Save")
            save_button.clicked.connect(self.save_changes)
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(self.reject)

            layout.addWidget(save_button, len(fields), 1)
            layout.addWidget(cancel_button, len(fields), 2)

        self.setLayout(layout)

    def edit_field(self, field, label):
        text, ok = QInputDialog.getText(
            self,
            f"Edit {label}",
            f"Enter new value for {label}:",
            QLineEdit.Normal,
            field.text()
        )
        if ok and text:
            field.setText(text)

    def save_changes(self):
        # Update the task object with the new values from the labels
        for label, field in self.field_labels.items():
            new_value = field.text()
            setattr(self.task, self._attribute_name(label), new_value)

        try:
            # Save the task using the task controller
            self.task_controller.update_task(self.task)  # Ensure this method exists
            self.accept()
        except Exception as e:
            # Handle any exceptions during the update
            # For example, show an error message
            error_dialog = QDialog(self)
            error_layout = QVBoxLayout()
            error_label = QLabel(f"Failed to update task: {e}")
            error_layout.addWidget(error_label)
            error_dialog.setLayout(error_layout)
            error_dialog.exec_()

    @staticmethod
    def _attribute_name(label):
        # Map label to task attribute names
        mapping = {
            'Kommun': 'kommun',
            'Adress': 'adress',
            'Ort': 'ort',
            'Material': 'material',
            'Tömningsfrekvens': 'tomningsfrekvens',
            'Status': 'status',
            'Info': 'info',
            'Chaufför': 'chauffor',
            'Koordinater': 'koordinater',
        }
        return mapping.get(label, label.lower())

