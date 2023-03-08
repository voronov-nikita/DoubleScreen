import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Window')
        # self.setGeometry(100, 100, 300, 200)

        button = QPushButton('Open New Window', self)
        button.setGeometry(100, 50, 100, 50)
        button.clicked.connect(self.open_new_window)

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()


class NewWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('New Window')
        self.setGeometry(200, 200, 300, 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
