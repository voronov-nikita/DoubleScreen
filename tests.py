import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog

class NewWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Установка размеров и заголовка нового окна
        self.setWindowTitle("New Window")
        self.setGeometry(100, 100, 200, 200)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Создание кнопки для открытия нового окна
        self.button = QPushButton("Open new window", self)
        self.button.clicked.connect(self.open_new_window)

    def open_new_window(self):
        # Создание объекта нового окна и его отображение
        new_window = NewWindow()
        new_window.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
