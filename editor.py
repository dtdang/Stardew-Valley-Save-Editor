import xml.etree.ElementTree as ET
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, os
import functools
import binascii
import struct


# Subclass QMainWindow to customize your application's main window
class SDVapp(QMainWindow):
    def __init__(self):
        super().__init__()
        global root
        root = QFileInfo(__file__).absolutePath()
        self.title = 'SDV Save Editor'
        self.setWindowIcon(QIcon(root + '/img/sdv.png'))
        width = 975
        height = 600
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.width = width
        self.height = height
        self.setFixedSize(width, height)
        self.initUI()

    def initUI(self):
        global root
        root = QFileInfo(__file__).absolutePath()
        self.setWindowTitle(self.title)

        ###Menu Bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')

        fileMenu_open = QAction(QIcon(root + '/img/open_file.png'), '&Open', self)
        fileMenu_open.setShortcut('Ctrl+O')
        fileMenu_open.setStatusTip('Open File')
        # fileMenu_open.triggered.connect(self.openfile)

        fileMenu_save = QAction(QIcon(root + '/img/save_file.png'), '&Save', self)
        fileMenu_save.setShortcut('Ctrl+S')
        fileMenu_save.setStatusTip('Save File')
        # fileMenu_save.triggered.connect(self.savefile)

        fileMenu_exit = QAction(QIcon(root + '/img/exit.png'), '&Exit', self)
        fileMenu_exit.setShortcut('Ctrl+Q')
        fileMenu_exit.setStatusTip('Exit')
        # fileMenu_exit.triggered.connect(qApp.quit)

        helpMenu_usage = QAction(QIcon(root + '/img/help.png'), '&How to use', self)
        helpMenu_usage.setShortcut('Ctrl+H')
        helpMenu_usage.setStatusTip('How to use')
        # helpMenu_usage.triggered.connect(self.show_howto)

        helpMenu_about = QAction(QIcon(root + '/img/about.png'), '&About', self)
        helpMenu_about.setStatusTip('About')
        # helpMenu_about.triggered.connect(self.show_about)

        fileMenu.addAction(fileMenu_open)
        fileMenu.addAction(fileMenu_save)
        fileMenu.addAction(fileMenu_exit)
        helpMenu.addAction(helpMenu_usage)
        helpMenu.addAction(helpMenu_about)

        self.show()

    @pyqtSlot()
    def openfile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', 'savedata')
        if filename[0] == '':
            return
        if (os.path.getsize(filename[0]) >= 2671000):
            f = open(filename[0], 'rb').read()
            global h
            h = (binascii.hexlify(f))
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Not a valid savefile!")
            msg.setWindowTitle("Not valid")
            msg.setWindowIcon(QIcon(root + '/img/icon.ico'))
            msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    ex = SDVapp()
    sys.exit(app.exec())