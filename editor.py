import xml.etree.ElementTree as ET
import xmltodict
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, os


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

        ## Toolbar
        toolbar = self.addToolBar("File")
        toolbar.setMovable(False)
        
        toolbar_openfile = QAction(QIcon(root + '/img/open_file.png'), 'Open File', self)
        toolbar_openfile.triggered.connect(self.openfile)

        toolbar_savefile = QAction(QIcon(root + '/img/save_file.png'), 'Save File', self)
        toolbar_savefile.triggered.connect(self.savefile)

        toolbar.addAction(toolbar_openfile)
        toolbar.addAction(toolbar_savefile)

        #Tabs
        centralWidget = QWidget(self)
        centralWidgetLayout = QVBoxLayout(centralWidget)
        centralWidget.setLayout(centralWidgetLayout)

        tabContainer = QTabWidget(centralWidget)

        tab1 = QWidget(tabContainer)
        tab2 = QWidget(tabContainer)
        tab3 = QWidget(tabContainer)
        tab4 = QWidget(tabContainer)
        tab5 = QWidget(tabContainer)

        tab1Layout = QVBoxLayout(tab1)
        tabContainer.setLayout(tab1Layout)
        tabContainer.addTab(tab1, "Player Settings")
        tabContainer.addTab(tab2, "Gameplay Data")
        tabContainer.addTab(tab3, "Skills")
        tabContainer.addTab(tab4, "Friendship")
        tabContainer.addTab(tab5, "Animals")

        tabContainer.setCurrentIndex(0)
        centralWidgetLayout.addWidget(tabContainer)
        self.setCentralWidget(centralWidget)


        self.show()
    
    #Open File
    @pyqtSlot()
    def openfile(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', os.path.join(os.getenv("APPDATA"), "StardewValley", "Saves"), "All Files (*.*)")[0]
        if self.filename == '':
            return
        with open(self.filename, 'rb') as f:
            self.xmldict = xmltodict.parse(f.read())
            f.close
            try:
                self.xmldict['SaveGame']
            except KeyError as e:
                raise e

    #Save file
    def savefile(self):
        if hasattr(self, "filename") and self.filename != None:
            savedir = QFileDialog.getSaveFileName(self, 'Save File', 'SaveData')[0]
            if savedir == '':
                return
            with open (savedir, 'w') as f:
                f.write(xmltodict.unparse(self.xmldict))
                f.close
            QMessageBox.information(self, "Saved", "Your Game has been saved!")
        else:
            QMessageBox.information(self, "No file to save", "Invaid save")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    ex = SDVapp()
    sys.exit(app.exec())