# database.test.task_testing_controller.py
import unittest
from controllers import (TaskController)

class TaskTestingController(unittest.TestCase):
    def setUp(self):
        self.controller = TaskController()

    def test_create_task_success(self):
        """Test creating a task with correct data."""
        data = {
            "kommun": "Test Kommun",
            "adress": "Test Adress",
            "ort": "Test Ort",
            "material": "Test Material",
            "tomningsfrekvens": "Måndag, Varje vecka",
            "next_occurrence_date": "2024-08-20"
        }
        result = self.controller.create_task(data)
        self.assertTrue(result)

    def test_create_task_with_invalid_date(self):
        """Test creating a task with an invalid date."""
        data = {
            "kommun": "Test Kommun",
            "adress": "Test Adress",
            "ort": "Test Ort",
            "material": "Test Material",
            "tomningsfrekvens": "Måndag, Varje vecka",
            "next_occurrence_date": "invalid-date"
        }
        with self.assertRaises(ValueError):
            self.controller.create_task(data)

    def test_create_task_with_invalid_frequency(self):
        """Test creating a task with an invalid frequency."""
        data = {
            "kommun": "Test Kommun",
            "adress": "Test Adress",
            "ort": "Test Ort",
            "material": "Test Material",
            "tomningsfrekvens": "Invalid Frequency",
            "next_occurrence_date": "2024-08-20"
        }
        with self.assertRaises(ValueError):
            self.controller.create_task(data)

if __name__ == '__main__':
    unittest.main()
