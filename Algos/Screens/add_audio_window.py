from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from enum import Enum
from simple_audio_recorder import SimpleAudioRecorder


WINDOW_HEIGHT = 500
WINDOW_WIDTH = 800


class AddAudioWindow(QMainWindow):

   def __init__(self, dest_directory): #isRecordingValue, responseValue
      super(AddAudioWindow,self).__init__()
      self.isRecording = False
      self.destDirectory = dest_directory
      self.audioRecorder = SimpleAudioRecorder(dest_directory)
      self.initUI()
      self.hideNextActions()

   def onButtonClicked(self):
      l = self.letterEdit.text()
      if self.isRecording == False and l != "" and l != None:
         self.isRecording = True
         self.recordButton.setText("Recording ...")
         self.recordButton.setStyleSheet('color: white; background-color: #B70000;')
         self.recordButton.adjustSize()
         self.hideActions()

         # Create filename TODO : modifier "truc" avec timestamp
         fname = l[0] + "_truc.wav"

         # Start recording audio
         self.audioRecorder.record(fname, 8)
         self.onRecordFinished()


   def onRecordFinished(self):
      self.recordButton.hide()
      self.isRecording = False
      self.showNextActions()

   def hideActions(self):
      self.intro.hide()
      self.intro2.hide()
      self.intro3.hide()
      self.letterEdit.hide()
      #self.recordButton.hide()

   def showActions(self):
      self.intro.show()
      self.intro2.show()
      self.intro3.show()
      self.letterEdit.setText("")
      self.letterEdit.show()
      self.recordButton.setText("Start")
      self.recordButton.setStyleSheet('color: white; background-color: #73C371;')
      self.recordButton.adjustSize()
      self.recordButton.show()

   def onConfirmClick(self):
      print("Confirm")
      # TODO : Process folder with new audios
      self.close()

   def onCancelClick(self):
      print("Canceled")
      self.audioRecorder.clearFiles()
      self.close()

   def onAddMoreClick(self):
      self.showActions()

   def showNextActions(self):
      self.confirmButton.show()
      self.addMoreButton.show()
      self.cancelButton.show()

   def hideNextActions(self):
      self.confirmButton.hide()
      self.addMoreButton.hide()
      self.cancelButton.hide()

   def initUI(self):
      self.setGeometry(500,300,WINDOW_WIDTH,WINDOW_HEIGHT)
      self.setWindowTitle("ClaviAI - Populate dataset")
      self.setMinimumWidth(WINDOW_WIDTH)
      self.setMaximumWidth(WINDOW_WIDTH)
      self.setMinimumHeight(WINDOW_HEIGHT)
      self.setMaximumHeight(WINDOW_HEIGHT)
      self.setStyleSheet('background-color: #403F4B;')

      self.intro = QLabel(self)
      self.intro.setText("Ici, vous pouvez ajouter l'audio d'une lettre de votre choix.")
      self.intro.adjustSize()
      self.intro.setStyleSheet('color: white;')
      self.intro.move(int(WINDOW_WIDTH/2) - int(self.intro.frameGeometry().width()/2), 50)


      self.intro2 = QLabel(self)
      self.intro2.setText("La lettre que vous allez tapper : ")
      self.intro2.adjustSize()
      self.intro2.setStyleSheet('color: white;')
      self.intro2.move(int(WINDOW_WIDTH/2) - int(self.intro2.frameGeometry().width()/2), 50 + (self.intro.frameGeometry().height()*2))

      self.letterEdit = QLineEdit(self)
      self.letterEdit.setStyleSheet('color: #73C371;') 
      self.letterEdit.move(int(WINDOW_WIDTH/2) + int(self.intro2.frameGeometry().width()/2), 50 + (self.intro.frameGeometry().height()*2))

      self.intro3 = QLabel(self)
      self.intro3.setText("Maintenant appuyez sur Start pour lancer un enregistrement de 8 secondes.\nAppuyez autant de fois que possible sur la touche renseignée tout en respectant\nun délais minimum de 0.5s entre chaque pression de touche.\nPs: appuyez différement sur la touche pour un meilleur résultat")
      self.intro3.adjustSize()
      self.intro3.setStyleSheet('color: white;')
      self.intro3.move(int(WINDOW_WIDTH/2) - int(self.intro3.frameGeometry().width()/2), 200)


      self.recordButton = QPushButton(self)
      self.recordButton.setText("Start")
      self.recordButton.setAttribute(Qt.WA_StyledBackground, True)
      self.recordButton.setStyleSheet('color: white; background-color: #73C371;')
      self.recordButton.adjustSize()
      self.recordButton.clicked.connect(self.onButtonClicked)
      self.recordButton.move(int(WINDOW_WIDTH/2) - int(self.recordButton.frameGeometry().width()/2), 300)



      self.cancelButton = QPushButton(self)
      self.cancelButton.setText("Annuler")
      self.cancelButton.setAttribute(Qt.WA_StyledBackground, True)
      self.cancelButton.setStyleSheet('color: white; background-color: #B70000;')
      self.cancelButton.adjustSize()
      self.cancelButton.clicked.connect(self.onCancelClick)
      self.cancelButton.move(int(WINDOW_WIDTH/2) + 30, WINDOW_HEIGHT - 60)

      self.confirmButton = QPushButton(self)
      self.confirmButton.setText("Confirmer")
      self.confirmButton.setAttribute(Qt.WA_StyledBackground, True)
      self.confirmButton.setStyleSheet('color: white; background-color: #73C371;')
      self.confirmButton.adjustSize()
      self.confirmButton.clicked.connect(self.onConfirmClick)
      self.confirmButton.move(int(WINDOW_WIDTH) - 10 - int(self.confirmButton.frameGeometry().width()), WINDOW_HEIGHT - 60)


      self.addMoreButton = QPushButton(self)
      self.addMoreButton.setText("Ajouter une lettre")
      self.addMoreButton.setAttribute(Qt.WA_StyledBackground, True)
      self.addMoreButton.setStyleSheet('color: white; background-color: #384077;')
      self.addMoreButton.adjustSize()
      self.addMoreButton.clicked.connect(self.onAddMoreClick)
      self.addMoreButton.move(int(WINDOW_WIDTH/2) - 30 - int(self.addMoreButton.frameGeometry().width()), WINDOW_HEIGHT - 60)

      
