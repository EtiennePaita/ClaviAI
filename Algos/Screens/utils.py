from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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


def align_object(qobject, alignment, WINDOW_WIDTH, WINDOW_HEIGHT):
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
      
