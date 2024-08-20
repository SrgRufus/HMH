# controller.task_controller.py

class TaskController:
    """
       Controller för att hantera uppdrag i applikationen.
       """

    def create_task(self, data):
        """
        Skapar ett nytt uppdrag med den givna datan.

        :param data: Dictionary med uppdragsdata.
        :return: True om uppdraget skapades, annars False.
        """