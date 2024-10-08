import sys
import requests
import assemblyai as aai
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QComboBox, QTextEdit, QFileDialog

# Установим API ключ для AssemblyAI
aai.settings.api_key = "96dae3cabdb9429194ffaf6ab5fdad27"

class SpeechToTextApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Speech to Text App")
        self.setGeometry(200, 200, 500, 400)

        # Компоненты интерфейса
        layout = QVBoxLayout()

        self.api_selector = QComboBox()
        self.api_selector.addItems(["Whisper", "AssemblyAI"])
        layout.addWidget(self.api_selector)

        self.file_label = QLabel("Файл не выбран")
        layout.addWidget(self.file_label)

        self.select_file_btn = QPushButton("Выбрать аудиофайл")
        self.select_file_btn.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_btn)

        self.transcribe_btn = QPushButton("Запустить расшифровку")
        self.transcribe_btn.clicked.connect(self.transcribe_audio)
        layout.addWidget(self.transcribe_btn)

        self.result_area = QTextEdit()
        layout.addWidget(self.result_area)

        self.central_widget = QLabel()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.selected_file = None

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Audio Files (*.mp3 *.wav)", options=options)
        if file_name:
            self.selected_file = file_name
            self.file_label.setText(f"Выбран файл: {file_name}")

    def transcribe_audio(self):
        selected_api = self.api_selector.currentText()

        if self.selected_file:
            if selected_api == "Whisper":
                self.transcribe_with_whisper(self.selected_file)
            elif selected_api == "AssemblyAI":
                self.transcribe_with_assembly(self.selected_file)
        else:
            self.result_area.setText("Пожалуйста, выберите файл.")

    def transcribe_with_whisper(self, file_name):
          url = "https://chatgpt-42.p.rapidapi.com/whisperv3"

          # Открываем файл в бинарном режиме
          with open(file_name, 'rb') as audio_file:
                    files = {
                                'file': (file_name, audio_file)  # Используем имя файла и объект файла
                    }
        
                    headers = {
                              "x-rapidapi-key": "0ae5ddb63emshf95aca092906310p105a1ajsne284f1fdcd7f",
                              "x-rapidapi-host": "chatgpt-42.p.rapidapi.com"
                    }

                    # Отправляем POST-запрос с файлом
                    response = requests.post(url, files=files, headers=headers)

                    print(response.json())

                    if response.status_code == 200:
                        result = response.json()
                        self.result_area.setText(result.get('text', 'Нет текста в ответе.'))
                    else:
                        self.result_area.setText(f"Ошибка: {response.status_code}, {response.text}")

    def transcribe_with_assembly(self, file_name):
        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(language_code="ru")
        transcript = transcriber.transcribe(file_name, config)
        if transcript.status == aai.TranscriptStatus.error:
                    self.result_area.setText(transcript.error)
        else:
                    self.result_area.setText(transcript.text)

# Запуск приложения
app = QApplication(sys.argv)
window = SpeechToTextApp()
window.show()
sys.exit(app.exec_())