import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QHBoxLayout, QPushButton

from db_connection.coffee_init_service import CoffeeProj


class CoffeeUi(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("coffee.ui")
        Init = self.ui.btn_init.clicked.connect(self.init)
        backup = self.ui.btn_backup.clicked.connect(self.backup)
        restore = self.ui.btn_restore.clicked.connect(self.restore)
        self.ui.show()

    def init(self):
        db = CoffeeProj()
        QMessageBox.about(self, 'init', 'init')
        db.service()

    def backup(self):
        db = CoffeeProj()
        QMessageBox.about(self, 'backup', 'backup')
        db.data_backup('product')
        db.data_backup('sale')



    def restore(self):
        QMessageBox.about(self, 'restore', 'restore')
        db = CoffeeProj()
        db.data_restore('product')
        db.data_restore('sale')


