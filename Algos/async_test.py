from multiprocessing import Process, Value, Manager
import ctypes
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from audio_recorder import AudioRecorder
import sys
from enum import Enum

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 800

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

   def __init__(self, isRecordingValue,responseValue):
      super(MyWindow,self).__init__()
      self.responseValue = responseValue
      self.isRecording = False
      self.isRecordingValue = isRecordingValue
      self.initUI()

   def startRecording(self):
      print("Start recording audio...")
      self.recordButton.setText("Stop")
      self.recordButton.adjustSize()
      
      self.isRecordingValue.value = 1
   def stopRecording(self):
      print("Stop recording audio")
      self.recordButton.setText("Start")
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

   def initUI(self):
      self.setGeometry(500,300,WINDOW_WIDTH,WINDOW_HEIGHT)
      self.setWindowTitle("ClaviAI")
      self.setMinimumWidth(WINDOW_WIDTH)
      self.setMaximumWidth(WINDOW_WIDTH)
      self.setMinimumHeight(WINDOW_HEIGHT)
      self.setMaximumHeight(WINDOW_HEIGHT)

      self.label = QLabel(self)
      self.label.setText("Texte généré : ")
      #self.label.adjustSize()
      #self.label.setAlignment(Qt.AlignCenter)
      self.label.move(int(WINDOW_WIDTH/2) - int(self.label.frameGeometry().width()/2), int(WINDOW_HEIGHT/2) - int(self.label.frameGeometry().height()/2))
      
      self.editText = QLineEdit(self)
      self.align_object(self.editText,Alignment.END_CENTER)
      #self.align_object(self.label, Alignment.CENTER)

      self.recordButton = QPushButton(self)
      self.recordButton.setText("Start")
      #self.recordButton.move(int(WINDOW_WIDTH/2) - (self.recordButton.frameGeometry().width()/2), int(WINDOW_HEIGHT - self.recordButton.frameGeometry().height()))
      self.recordButton.clicked.connect(self.onButtonClicked)
      self.align_object(self.label,Alignment.CENTER)

      self.generateTextLabel = QLabel(self)
      self.generateTextLabel.resize(400, 400) 
      
      #
      # TODO : find a way to refresh the screen
      #
      self.generateTextLabel.setText(f"{self.responseValue.value}")
      #

      #self.align_object(self.label,Alignment.BOTTOM_CENTER)
      self.generateTextLabel.move(int(WINDOW_WIDTH/2) - int(self.generateTextLabel.frameGeometry().width()/2), WINDOW_HEIGHT - int(self.generateTextLabel.frameGeometry().height()))

def window(isRecordingValue, responseValue):
   app = QApplication(sys.argv)
   win = MyWindow(isRecordingValue,responseValue)
   win.show()
   sys.exit(app.exec_())


def main():
   manager = Manager()
   a = AudioRecorder("./", "./")
   isRecordingValue = Value('i', 0)
   responseValue = manager.Value(ctypes.c_wchar_p, "H")

   appProcess = Process(target=window, args =(isRecordingValue,responseValue,))
   
   audioProcess = Process(target=a.build, args =(isRecordingValue,responseValue,))
   audioProcess.daemon = True               # daemon threads will be destroy when main process ends
   
   audioProcess.start()
   appProcess.start()
   appProcess.join()     
   print(f"{responseValue.value}")             # join process to wait until it ends
    


if __name__ == "__main__":
   main()