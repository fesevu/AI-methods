from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QWidget

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
        self.api_combo.addItems(['AssemblyAI', 'Google Speech API'])
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
            # Здесь будет логика отправки файла на выбранный API
            self.result_text.setText(f"Файл загружен: {file_name}")

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
