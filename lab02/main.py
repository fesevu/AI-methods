import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit
from transformers import pipeline

# Инициализация модели ruGPT3Small
chat_model = pipeline('text-generation', model='ai-forever/rugpt3small_based_on_gpt2')

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Чат с ruGPT3Small')
        self.setGeometry(100, 100, 500, 400)

        # Создание элементов интерфейса
        self.layout = QVBoxLayout()
        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText('Введите сообщение и нажмите Enter...')
        self.chat_input.returnPressed.connect(self.handle_input)

        # Добавление элементов на форму
        self.layout.addWidget(self.chat_output)
        self.layout.addWidget(self.chat_input)
        self.setLayout(self.layout)

    def handle_input(self):
        # Получение текста из окна ввода
        user_input = self.chat_input.text().strip()
        if user_input:
            # Отображение сообщения пользователя
            self.chat_output.append(f'Вы: {user_input}')

            # Генерация ответа модели
            response = chat_model(user_input, max_length=100, num_return_sequences=1)
            model_response = response[0]['generated_text'][len(user_input):].strip()

            # Отображение ответа модели
            self.chat_output.append(f'ruGPT3Small: {model_response}\n')

            # Очистка окна ввода
            self.chat_input.clear()

def main():
    app = QApplication(sys.argv)
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
