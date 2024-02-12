from PyQt5 import QtCore, QtGui, QtWidgets
from multiprocessing import Process, Manager
import ctypes
from audio_recorder import AudioRecorder
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 430, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(250, 80, 241, 31))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 260, 291, 101))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setReadOnly(True) 
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 230, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(220, 20, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.isRecording = False
        self.responseValue = ""

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.updateUI)
        self.timer.start()

        self.manager = Manager()
        self.responseValue = self.manager.Value(ctypes.c_wchar_p, "")
        self.isRecordingValue = self.manager.Value('i', 0)

        self.a = AudioRecorder("./")
        self.audioProcess = Process(target=self.a.build, args=(self.isRecordingValue, self.responseValue,))
        self.audioProcess.daemon = True
        self.audioProcess.start()

        self.pushButton.clicked.connect(self.onButtonClicked)

    def onButtonClicked(self):
        if self.isRecording:
            self.isRecording = False
            self.stopRecording()
        else:
            self.isRecording = True
            self.startRecording()

    def startRecording(self):
        print("Start recording audio...")
        self.pushButton.setText("Stop")
        self.pushButton.setStyleSheet('color: white; background-color: #B70000;')
        self.pushButton.adjustSize()
        self.isRecordingValue.value = 1

    def stopRecording(self):
        print("Stop recording audio")
        self.pushButton.setText("Start")
        self.pushButton.setStyleSheet('background-color: #73C371;')
        self.pushButton.adjustSize()
        self.isRecordingValue.value = 0

    def updateUI(self):
        self.lineEdit_2.setText(f"{self.responseValue.value}")
        self.lineEdit_2.adjustSize()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "Prédictions : "))
        self.label_2.setText(_translate("MainWindow", "Tapez vos lettres !"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
