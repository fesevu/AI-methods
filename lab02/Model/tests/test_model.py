import unittest
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