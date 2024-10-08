import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QWidget
import time

class SpeechToTextApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Выпадающий список для выбора API
        self.api_label = QLabel('Выберите API:', self)
        layout.addWidget(self.api_label)

        self.api_combo = QComboBox(self)
        self.api_combo.addItems(['AssemblyAI', 'Rev AI'])
        layout.addWidget(self.api_combo)

        # Кнопка для загрузки файла
        self.upload_button = QPushButton('Загрузить аудиофайл', self)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        # Текстовое поле для отображения результата
        self.result_label = QLabel('Распознанный текст:', self)
        layout.addWidget(self.result_label)

        self.result_text = QTextEdit(self)
        layout.addWidget(self.result_text)

        # Кнопка для сохранения результата в файл
        self.save_button = QPushButton('Сохранить текст в файл', self)
        self.save_button.clicked.connect(self.save_text)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.setWindowTitle('Speech to Text Converter')
        self.setGeometry(300, 300, 400, 300)

    def upload_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите аудиофайл", "", "Audio Files (*.mp3 *.wav)", options=options)
        if file_name:
            selected_api = self.api_combo.currentText()
            if selected_api == 'AssemblyAI':
                result = self.call_assemblyai(file_name)
            elif selected_api == 'Rev AI':
                result = self.call_revai(file_name)
            
            self.result_text.setText(result)

    def call_assemblyai(self, file_name):
        url = "https://assemblyai-speech-to-text.p.rapidapi.com/"
        headers = {
            "x-rapidapi-key": "0ae5ddb63emshf95aca092906310p105a1ajsne284f1fdcd7f",
            "x-rapidapi-host": "assemblyai-speech-to-text.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        
        # Чтение аудиофайла для отправки в API
        with open(file_name, 'rb') as f:
            audio_data = f.read()

        response = requests.post(url, data=audio_data, headers=headers)
        if response.status_code == 200:
            return response.json().get('text', 'Текст не найден')
        else:
            return f"Ошибка: {response.status_code}, {response.text}"

    def call_revai(self, file_name):
        # Шаг 1: Создание задачи для распознавания
        job_url = "https://rev-ai.p.rapidapi.com/jobs"
        headers = {
            "x-rapidapi-key": "0ae5ddb63emshf95aca092906310p105a1ajsne284f1fdcd7f",
            "x-rapidapi-host": "rev-ai.p.rapidapi.com",
        }

        with open(file_name, 'rb') as f:
            files = {'media': f}
            response = requests.post(job_url, files=files, headers=headers)

        if response.status_code != 200:
            return f"Ошибка при создании задачи: {response.status_code}, {response.text}"

        job_id = response.json().get('id')
        
        # Шаг 2: Ожидание завершения задачи и получение результата
        transcript_url = f"https://rev-ai.p.rapidapi.com/jobs/{job_id}/transcript"
        headers = {
            "x-rapidapi-key": "0ae5ddb63emshf95aca092906310p105a1ajsne284f1fdcd7f",
            "x-rapidapi-host": "rev-ai.p.rapidapi.com",
            "Accept": "application/vnd.rev.transcript.v1.0+json"
        }

        # Проверка статуса задачи (polling)
        status_url = f"https://rev-ai.p.rapidapi.com/jobs/{job_id}"
        while True:
            status_response = requests.get(status_url, headers=headers)
            status = status_response.json().get('status')
            if status == 'transcribed':
                break
            elif status == 'failed':
                return "Ошибка: Задача не была выполнена."
            time.sleep(5)  # Подождать 5 секунд перед следующей проверкой

        # Получение транскрипта
        transcript_response = requests.get(transcript_url, headers=headers)
        if transcript_response.status_code == 200:
            return transcript_response.json().get('monologues')[0].get('elements')[0].get('value', 'Текст не найден')
        else:
            return f"Ошибка при получении транскрипта: {transcript_response.status_code}, {transcript_response.text}"

    def save_text(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить текст как", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.result_text.toPlainText())

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = SpeechToTextApp()
    ex.show()
    sys.exit(app.exec_())
