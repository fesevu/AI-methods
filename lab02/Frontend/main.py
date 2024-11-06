import sys
from PyQt5.QtWidgets import QApplication
from interface import ChatWindow


def main() -> None:
    """
    Запуск основного приложения.
    """
    app = QApplication(sys.argv)
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
