import sys
import qdarkstyle
from PyQt5.QtSql import *
from PyQt5.QtCore import Qt, QModelIndex,QSize, pyqtSignal,QRect,QMetaObject,QCoreApplication
from PyQt5.QtWidgets import QMainWindow,QWidget, QApplication,QVBoxLayout,QStatusBar,QPlainTextEdit,QPushButton,QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout
from PyQt5.QtGui import QImage, qRgb, QPixmap ,QIcon
import Recognition_Manage as rm
import Face_recognizer as fr
import Database_manager as dm
import cv2

class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.ab = dm.Database_manage()
        self.ab.init('HCI_Database', 'QSQLITE')
        self.f = fr.Face_Thread()
        self.r = rm.Rec_Thread()
        self.num_iter = 0
        self.setupUi(self)
        self.setFixedSize(320, 380)

    def setupUi(self, Ui_MainWindow):
        Ui_MainWindow.setObjectName("Spotify Assistant")
        Ui_MainWindow.resize(320, 380)
        self.centralwidget = QWidget(Ui_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mic_button = QPushButton(self.centralwidget)
        self.mic_button.setGeometry(QRect(70, 290, 45, 45))
        self.mic_button.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/mic_on.png"))
        self.mic_button.setIcon(icon)
        self.mic_button.setIconSize(QSize(44, 43))
        self.mic_button.setObjectName("mic_button")
        self.rec_button = QPushButton(self.centralwidget)
        self.rec_button.setGeometry(QRect(145, 290, 45, 45))
        self.rec_button.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("icons/video.png"))
        self.rec_button.setIcon(icon1)
        self.rec_button.setIconSize(QSize(43, 43))
        self.rec_button.setObjectName("rec_button")
        self.data_button = QPushButton(self.centralwidget)
        self.data_button.setGeometry(QRect(215, 305, 30, 30))
        self.data_button.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/add_data.png"))
        self.data_button.setIcon(icon)
        self.data_button.setIconSize(QSize(28, 28))
        self.data_button.setObjectName("mic_button")
        self.suggestion_box = QPlainTextEdit(self.centralwidget)
        self.suggestion_box.setUndoRedoEnabled(False)
        self.suggestion_box.setReadOnly(True)
        self.suggestion_box.setGeometry(QRect(30, 40, 261, 231))
        self.suggestion_box.setObjectName("suggestion_box")
        self.suggestion_box.setPlainText('Ciao ' + self.r.name +' \n\nPotresti utilizzare i seguenti comandi: \n' + '-start \n' + '-stop \n'+ '-next track \n' + '-previous track \n'
                                         + '-repeat(+ track/ + all/ + off) \n' + '-shuffle (+ on/off) \n'+ '-down volume \n' + '-up volume \n'
                                         + '-play (+ name artist or track) \n'+ '-play (+ album name) album \n'
                                         + '-play (+ playlist name) playlist \n'+ '-play my tracks \n'+ '-italian language \n'+ '-english language\n')
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(100, 10, 121, 21))
        self.label.setObjectName("label")
        Ui_MainWindow.setCentralWidget(self.centralwidget)
        self.mic_button.clicked.connect(self.start_rec, type=Qt.QueuedConnection)
        self.rec_button.clicked.connect(self.start_video, type=Qt.QueuedConnection)
        self.data_button.clicked.connect(self.Database_access, type=Qt.QueuedConnection)

        self.retranslateUi(Ui_MainWindow)
        QMetaObject.connectSlotsByName(Ui_MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spotify Assistant"))
        self.label.setText(_translate("MainWindow", " Spotify Assistant"))

    def unreco_register(self):
        if(self.num_iter==1):
            buttonReply=QMessageBox.question(self,'Unknown','Sign In', QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.Database_access()


    def start_video(self):
        self.num_iter = self.num_iter + 1
        self.f.reco.connect(self.Suggestion)
        #self.f.unreco.connect(self.unreco_register)
        self.f.face_rec_loop()
        self.num_iter = self.num_iter - 1

    def start_rec(self):
        if(self.r.active == True):
            self.changeBottonIcon("icons/mic_on.png")
            self.r.deactivate()
        else:
            self.changeBottonIcon("icons/mic_offf.png")
            self.r.listen_loop()

    def Database_access(self):
        self.ab.show()

    def Suggestion(self, username):
        c=self.ab.get_user(username)
        self.suggestion_box.clear()
        self.suggestion_box.setPlainText('Ciao '+ username +'\n\nPotresti ascoltare:\n'+ 'Track: '+ c[0] +'\n'+'Artist: ' + c[1] +'\n\nPotresti utilizzare i seguenti comandi: \n' + '-start \n' + '-stop \n'+ '-next track \n' + '-previous track \n'
                                         + '-repeat (+ track/ + all/ + off) \n' + '-shuffle (+ on/off) \n'+ '-down volume \n' + '-up volume \n'
                                         + '-play (+ name artist or track) \n'+ '-play (+ album name) album \n'
                                         + '-play (+ playlist name) playlist \n'+ '-play my tracks \n'+ '-italian language \n'+ '-english language\n')

    def changeBottonIcon(self, path):
        icon = QIcon()
        icon.addPixmap(QPixmap(path))
        self.mic_button.setIcon(icon)
        self.mic_button.setIconSize(QSize(44, 43))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mw = Ui_MainWindow()
    mw.show()
    sys.exit(app.exec_())