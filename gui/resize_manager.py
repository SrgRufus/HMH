# gui/resize_manager.py : Denna fil hanterar hur olika element i programmet förändras i storlek när fönstret ändrar storlek
from PyQt5.QtWidgets import QSizePolicy  # Importera QSizePolicy som bestämmer hur widgets ändrar storlek

class ResizeManager:
    def __init__(self):
        """Den här metoden körs när vi skapar ett ResizeManager-objekt, men just nu gör den inget speciellt."""
        pass

    @staticmethod
    def apply_resize_policy(widget, h_policy=QSizePolicy.Expanding, v_policy=QSizePolicy.Expanding):
        """
        Den här metoden tilldelar en storlekspolicy till en widget.
        h_policy bestämmer hur widgeten ska ändra storlek horisontellt, och v_policy för vertikalt.
        """
        widget.setSizePolicy(h_policy, v_policy)  # Här tilldelas den faktiska storlekspolicyn till widgeten

    def resize_create_task_dialog(self, dialog):
        """Den här metoden justerar storleken på alla element i dialogen för att skapa en uppgift."""
        # Här skapas en lista över alla inmatningsfält och etiketter i dialogen
        input_widgets = [
            dialog.kommun_input, dialog.adress_input, dialog.ort_input,
            dialog.chauffor_input, dialog.tomningsfrekvens_dropdown,
            dialog.material_dropdown, dialog.koordinater_input,
            dialog.info_input
        ]

        # Alla dessa fält ska kunna expandera horisontellt, men ska bibehålla fast höjd
        for widget in input_widgets:
            self.apply_resize_policy(widget, QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Info-fältet ska kunna expandera både horisontellt och vertikalt
        self.apply_resize_policy(dialog.info_input, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Här hanteras storleksändringar för etiketterna (labels) så att de håller en fast storlek
        label_widgets = [
            dialog.kommun_label, dialog.adress_label, dialog.ort_label,
            dialog.chauffor_label, dialog.tomningsfrekvens_label,
            dialog.material_label, dialog.koordinater_label, dialog.info_label
        ]

        for label in label_widgets:
            self.apply_resize_policy(label, QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Ser till att submit-knappen har en lämplig storlek
        self.apply_resize_policy(dialog.submit_button, QSizePolicy.Fixed, QSizePolicy.Fixed)

    def resize_list_tasks(self, list_tasks):
        """Den här metoden justerar storleken på elementen i sidan som visar alla uppgifter."""
        self.apply_resize_policy(list_tasks.task_tree, QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resize_main_window(self, main_window):
        """Den här metoden justerar storleken på elementen i huvudfönstret."""
        self.apply_resize_policy(main_window.stacked_widget, QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resize_custom_buttons(self, button_layout):
        """Den här metoden justerar storleken på anpassade knappar."""
        for i in range(button_layout.count()):
            button = button_layout.itemAt(i).widget()
            if button:
                self.apply_resize_policy(button, QSizePolicy.Fixed, QSizePolicy.Fixed)
