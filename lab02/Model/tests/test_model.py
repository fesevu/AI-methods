import unittest
import sys
import os
sys.path.append(os.path.abspath(
    "D:\\Lab_sem_7\\AI methods\\AI-methods\\lab02\\Model"))
from generation import generate_response


class TestModel(unittest.TestCase):
    def test_response(self) -> None:
        """
        Тестирование функции генерации ответа модели.
        """
        user_input: str = "Привет, как дела?"
        response: str = generate_response(user_input)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)


if __name__ == '__main__':
    unittest.main()
