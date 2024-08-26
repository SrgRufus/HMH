# database.test.task_testing_controller.py
import unittest  # Importerar unittest-modulen som ger tillgång till att skriva och köra tester
from controllers import TaskController  # Importera TaskController för att testa

# Skapar en klass som innehåller tester för TaskController
class TaskTestingController(unittest.TestCase):
    def setUp(self):
        """Den här metoden körs före varje test och sätter upp det vad som behöves testas."""
        self.controller = TaskController()  # Skapar en instans av TaskController för att testa.

    def test_create_task_success(self):
        """Testar att skapa en uppgift med korrekt data."""
        data = {
            "kommun": "Test Kommun",
            "adress": "Test Adress",
            "ort": "Test Ort",
            "material": "Test Material",
            "tomningsfrekvens": "Måndag, Varje vecka",
            "next_occurrence_date": "2024-08-20"
        }
        result = self.controller.create_task(data)  # Försöker skapa en uppgift med korrekt data
        self.assertTrue(result)  # Kontrollera att uppgiften skapades framgångsrikt

    def test_create_task_with_invalid_date(self):
        """Testar att skapa en uppgift med ett ogiltigt datum."""
        data = {
            "kommun": "Test Kommun",
            "adress": "Test Adress",
            "ort": "Test Ort",
            "material": "Test Material",
            "tomningsfrekvens": "Måndag, Varje vecka",
            "next_occurrence_date": "invalid-date"  # Detta är ett ogiltigt datum
        }
        with self.assertRaises(ValueError):  # Förväntar att se ett ValueError som kastas
            self.controller.create_task(data)

    def test_create_task_with_invalid_frequency(self):
        """Testar att skapa en uppgift med en ogiltig tömningsfrekvens."""
        data = {
            "kommun": "Test Kommun",
            "adress": "Test Adress",
            "ort": "Test Ort",
            "material": "Test Material",
            "tomningsfrekvens": "Invalid Frequency",  # Detta är en ogiltig frekvens
            "next_occurrence_date": "2024-08-20"
        }
        with self.assertRaises(ValueError):  # Förväntar att se ett ValueError som kastas
            self.controller.create_task(data)

# Om den här filen körs direkt, startar testerna
if __name__ == '__main__':
    unittest.main()  # Kör alla tester i den här filen

