import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


app = QApplication(sys.argv)

mw = QWidget()
mw.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
mw.setWindowTitle('Main')
mw.resize(250, 150)
mw.show()

sys.exit(app.exec_())