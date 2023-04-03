import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

    def closeEvent(self, event):
        reply = self.question_dialog("Quit", "Are you sure you want to quit?")
        if reply == "yes":
            print(reply)
            event.accept()
        else:
            event.ignore()


    def question_dialog(self, title, message):
        reply = self.question(title, message)
        return reply.text()

    def question(self, title, message):
        return self.MessageBox().question(self, title, message)

    def MessageBox(self):
        return self.msgBox()

    def msgBox(self):
        return self.MessageBoxConstructor()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
