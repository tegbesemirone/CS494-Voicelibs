from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(1000, 200, 600, 600)
    win.setWindowTitle("Voice-Libs")

    win.show()
    sys.exit(app.exec_())
window()