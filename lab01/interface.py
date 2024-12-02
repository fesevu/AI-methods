from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from integration import transcribe_with_whisper, transcribe_with_assembly


class TranscribeThread(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self, file_name, api):
        super().__init__()
        self.file_name = file_name
        self.api = api

    def run(self):
        if self.api == "Whisper":
            result = transcribe_with_whisper(self.file_name)
        elif self.api == "AssemblyAI":
            result = transcribe_with_assembly(self.file_name)
        else:
            result = "Неверный выбор API."
        self.result_ready.emit(result)


class SpeechToTextApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        print("Инициализация SpeechToTextApp...")
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

        self.transcribe_btn = QPushButton("Начать расшифровку")
        self.transcribe_btn.clicked.connect(self.transcribe_audio)
        layout.addWidget(self.transcribe_btn)

        self.result_area = QTextEdit()
        layout.addWidget(self.result_area)

        self.central_widget = QLabel()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.selected_file: str = ""

    def select_file(self) -> None:
        """
        Функция для открытия диалогового окна и выбора аудиофайла.
        Устанавливает выбранный путь к файлу в self.selected_file.
        """
        print("Открытие диалогового окна для выбора аудиофайла...")
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл", "", "Аудиофайлы (*.mp3 *.wav)", options=options)
        if file_name:
            self.selected_file = file_name
            self.file_label.setText(f"Выбран файл: {file_name}")
            print(f"Выбран файл: {file_name}")
        else:
            print("Файл не выбран.")

    def transcribe_audio(self) -> None:
        """
        Функция для расшифровки выбранного аудиофайла с использованием выбранного API (Whisper или AssemblyAI).
        Отображает расшифрованный текст в текстовом поле результата.
        """
        selected_api = self.api_selector.currentText()
        print(f"Выбранный API для расшифровки: {selected_api}")

        if self.selected_file:
            print(f"Начало расшифровки для файла: {self.selected_file}")
            self.thread = TranscribeThread(self.selected_file, selected_api)
            self.thread.result_ready.connect(self.display_result)
            self.thread.start()
        else:
            self.result_area.setText("Пожалуйста, выберите файл.")
            print("Файл для расшифровки не выбран.")

    def display_result(self, result: str) -> None:
        """
        Функция для отображения результата расшифровки.
        """
        self.result_area.setText(result)
        print(f"Результат расшифровки: {result}")
