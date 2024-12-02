import sys
from PyQt5.QtWidgets import QApplication
from interface import SpeechToTextApp

# Запуск приложения


def main():
    print("Запуск приложения...")
    app = QApplication(sys.argv)
    window = SpeechToTextApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
