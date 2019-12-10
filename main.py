import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QWidget

from PyQt5.QtWidgets import QApplication

from database_setting.coffee import CoffeeUi


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = CoffeeUi()
    sys.exit(app.exec())
