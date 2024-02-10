from multiprocessing import Process, Manager
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from audio_recorder import AudioRecorder
import sys
from enum import Enum

WINDOW_HEIGHT = 1500 #500
WINDOW_WIDTH = 1500 #800

class Alignment(Enum):
   TOP_START = 1
   TOP_CENTER = 2
   TOP_END = 3
   END_CENTER = 4
   BOTTOM_SART = 5
   BOTTOM_CENTER = 6
   BOTTOM_END = 7
   START_CENTER = 8
   CENTER = 9

class MyWindow(QMainWindow):

   def __init__(self, isRecordingValue, responseValue):
      super(MyWindow,self).__init__()
      self.responseValue = responseValue
      self.isRecording = False
      self.isRecordingValue = isRecordingValue
      self.initUI()

      # create Timer to trigger the updateUI function each X millis
      self.timer = QTimer(self)
      self.timer.setSingleShot(False)
      self.timer.setInterval(300) # in milliseconds, so 5000 = 5 seconds
      self.timer.timeout.connect(self.updateUI)
      self.timer.start()

   def startRecording(self):
      print("Start recording audio...")
      self.recordButton.setText("Stop")
      self.recordButton.setStyleSheet('color: white; background-color: #B70000;')
      self.recordButton.adjustSize()
      
      self.isRecordingValue.value = 1

   def stopRecording(self):
      print("Stop recording audio")
      self.recordButton.setText("Start")
      
      self.recordButton.setStyleSheet('color: white; background-color: #73C371;')
      self.recordButton.adjustSize()

      self.isRecordingValue.value = 0

   def onButtonClicked(self):
      if self.isRecording == True:
         self.isRecording = False
         self.stopRecording()
      else:
         self.isRecording = True
         self.startRecording()

   #qobject.move(int(WINDOW_WIDTH/2) - int(self.recordButton.frameGeometry().width()/2), int(WINDOW_HEIGHT - int(self.recordButton.frameGeometry().height())))
   def align_object(self, qobject, alignment):
      if alignment == Alignment.TOP_START:
         qobject.move(0, 0)
      elif alignment == Alignment.TOP_CENTER:
         qobject.move(int(WINDOW_WIDTH/2) - int(qobject.frameGeometry().width()/2), 0)
      elif alignment == Alignment.TOP_END:
         qobject.move(WINDOW_WIDTH - int(qobject.frameGeometry().width()), 0)
      elif alignment == Alignment.END_CENTER:
         qobject.move(WINDOW_WIDTH - int(qobject.frameGeometry().width()), int(WINDOW_HEIGHT/2) - int(qobject.frameGeometry().height()/2))
      elif alignment == Alignment.BOTTOM_SART:
         qobject.move(0, WINDOW_HEIGHT - int(qobject.frameGeometry().height()))
      elif alignment == Alignment.BOTTOM_CENTER:
         qobject.move(int(WINDOW_WIDTH/2) - int(qobject.frameGeometry().width()/2), WINDOW_HEIGHT - int(qobject.frameGeometry().height()))
      elif alignment == Alignment.BOTTOM_END:
         qobject.move(WINDOW_WIDTH - int(qobject.frameGeometry().width()), WINDOW_HEIGHT - int(qobject.frameGeometry().height()))
      elif alignment == Alignment.START_CENTER:
         qobject.move(0, int(WINDOW_HEIGHT/2) - int(qobject.frameGeometry().height()/2))
      elif alignment == Alignment.CENTER:
         qobject.move(int(WINDOW_WIDTH/2) - int(qobject.frameGeometry().width()/2), int(WINDOW_HEIGHT/2) - int(qobject.frameGeometry().height()/2))

   def updateUI(self):
      self.generateTextLabel.setText(f"{self.responseValue.value}")

   def initUI(self):
      self.setGeometry(500,300,WINDOW_WIDTH,WINDOW_HEIGHT)
      self.setWindowTitle("ClaviAI")
      self.setMinimumWidth(WINDOW_WIDTH)
      self.setMaximumWidth(WINDOW_WIDTH)
      self.setMinimumHeight(WINDOW_HEIGHT)
      self.setMaximumHeight(WINDOW_HEIGHT)
      self.setStyleSheet('background-color: #403F4B;')

      self.label = QLabel(self)
      self.label.setText("Texte généré : ")
      self.label.adjustSize()
      self.label.setStyleSheet('color: white;')
      #self.label.setAlignment(Qt.AlignCenter)
      self.label.move(int(WINDOW_WIDTH/2) - int(self.label.frameGeometry().width()/2), int(WINDOW_HEIGHT/2) - int(self.label.frameGeometry().height()/2))
      #self.align_object(self.label,Alignment.CENTER)

      self.editText = QLineEdit(self)
      self.align_object(self.editText,Alignment.TOP_CENTER)
      self.editText.setStyleSheet('color: white;') 
      #self.align_object(self.label, Alignment.CENTER)

      self.recordButton = QPushButton(self)
      self.recordButton.setText("Start")

      self.recordButton.setAttribute(Qt.WA_StyledBackground, True)
      self.recordButton.setStyleSheet('color: white; background-color: #73C371;')

      self.recordButton.adjustSize()
      #self.recordButton.move(int(WINDOW_WIDTH/2) - (self.recordButton.frameGeometry().width()/2), int(WINDOW_HEIGHT - self.recordButton.frameGeometry().height()))
      self.recordButton.clicked.connect(self.onButtonClicked)
      self.align_object(self.recordButton,Alignment.TOP_START)

      self.generateTextLabel = QLabel(self)
      self.generateTextLabel.setAlignment(Qt.AlignCenter)
      self.generateTextLabel.resize(400, 400) 
      self.generateTextLabel.setStyleSheet('color: white;')
      
      self.generateTextLabel.setText(f"{self.responseValue.value}")

      #self.align_object(self.label,Alignment.BOTTOM_CENTER)
      self.generateTextLabel.move(int(WINDOW_WIDTH/2) - int(self.generateTextLabel.frameGeometry().width()/2), WINDOW_HEIGHT - int(self.generateTextLabel.frameGeometry().height()))


def windowProc(isRecordingValue,responseValue):
   # Initialisation de l'app QT
   app = QApplication(sys.argv)
   app.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
   window = MyWindow(isRecordingValue, responseValue)
   window.show()
   sys.exit(app.exec_())


def main():

   # Creation d'un manager de variable partagez entre les process
   manager = Manager()

   # initialisation variables partagées
   responseValue = manager.Value(ctypes.c_wchar_p, "Test")
   isRecordingValue = manager.Value('i', 0)

   # instancie Audiorecorder
   a = AudioRecorder("./")

   # Creation des process
   appProcess = Process(target=windowProc, args =(isRecordingValue,responseValue,))
   audioProcess = Process(target=a.build, args =(isRecordingValue,responseValue,))

   audioProcess.daemon = True                # daemon threads will be destroy when main process ends
   
   audioProcess.start()
   appProcess.start()
   appProcess.join()                         # join process to wait until it ends
   print(f"{responseValue.value}")             
    


if __name__ == "__main__":
   main()