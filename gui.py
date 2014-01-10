# -*- coding: utf-8 -*-

import sys
import thread
import color

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class GUI(QtGui.QWidget):
    
    def __init__(self):
        super(GUI, self).__init__()
        
        self.initUI()
        
    def btnVoiceClicked(self, arg) :
        if(self.btnVoice.isChecked() == True) :
            self.emit(QtCore.SIGNAL('listen()'))
        else:
            self.emit(QtCore.SIGNAL('recognize()'))
        self.btnVoice.repaint()

    def initUI(self):
        
        iiisLabel = QtGui.QLabel("hello")
        iiisLabel.setPixmap(QtGui.QPixmap(QString.fromUtf8("resource/iiis.png")));

        self.msgBox = QtGui.QTextEdit()
        self.msgBox.setReadOnly(True)
        # msgBox.setTextBackgroundColor(QColor(0, 0, 0))

        self.msgInput = QtGui.QLineEdit()
        self.btnVoice = QtGui.QPushButton()
        self.btnVoice.setFlat(True)
        self.btnVoice.setCheckable(True)
        self.btnVoice.setIcon(QIcon("resource/Speech Recognition.png"))
        self.btnVoice.setIconSize(QSize(64, 64))
        self.btnVoice.setStyleSheet("QPushButton:checked { background-color: red; }")
        self.btnVoice.setChecked(False)
        self.btnVoice.clicked.connect(self.btnVoiceClicked)
        self.btnVoice.repaint()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(iiisLabel, 1, 1)
        grid.addWidget(self.msgBox, 2, 1)

        grid2 = QtGui.QGridLayout()
        grid.addLayout(grid2, 3, 1)
        grid2.addWidget(self.msgInput, 1, 1)
        grid2.addWidget(self.btnVoice, 1, 2)
        
        self.setLayout(grid) 
        
        self.setGeometry(0, 0, 500, 800)
        self.setWindowTitle('YaoTalk')    
        self.show()
        self.raise_()
        self.activateWindow()

    def display(self, message, color):
    	# self.msgBox.setText("hi")
    	self.msgBox.setHtml(self.msgBox.toHtml()+u"<font family='helvetica' color='"+color+u"'>"+message+u'</>\n')
        self.repaint()
    	return None

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            self.btnVoice.click()
        # else:
            # super.keyPressEvent(qKeyEvent)

        
