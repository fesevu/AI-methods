import sys
import os
import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit

# Добавляем путь к Model для импорта generation.py
sys.path.append(os.path.abspath(
    "D:\\Lab_sem_7\\AI methods\\AI-methods\\lab02\\Model"))
from generation import generate_response

# Настройка логирования
logging.basicConfig(filename='D:\\Lab_sem_7\\AI methods\\AI-methods\\lab02\\Model\\logs\\chat_log.txt',
                    level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')


class ChatWindow(QWidget):
    def __init__(self) -> None:
        """
        Инициализация окна чата.
        """
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """
        Настройка пользовательского интерфейса.
        """
        self.setWindowTitle('Чат с ruGPT3Small')
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout()
        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText(
            'Введите сообщение и нажмите Enter...')
        self.chat_input.returnPressed.connect(self.handle_input)

        self.layout.addWidget(self.chat_output)
        self.layout.addWidget(self.chat_input)
        self.setLayout(self.layout)

    def handle_input(self) -> None:
        """
        Обработка ввода пользователя и генерация ответа модели.
        """
        user_input: str = self.chat_input.text().strip()
        if user_input:
            # Логирование пользовательского ввода
            logging.info(f'User: {user_input}')

            try:
                # Генерация ответа модели без хранения истории
                model_response: str = generate_response(user_input)
                self.chat_output.append(f'Вы: {user_input}')
                self.chat_output.append(f'ruGPT3Small: {model_response}\n')

                # Логирование ответа модели
                logging.info(f'ruGPT3Small: {model_response}')

            except Exception as e:
                # Логирование ошибок
                logging.error(f'Error generating response: {e}')
                self.chat_output.append(
                    'Ошибка при генерации ответа. Пожалуйста, попробуйте снова.')

            self.chat_input.clear()
