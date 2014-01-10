# coding: utf-8

from gui import *
import thread
import color
import time
import os 

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import YaoSpeech
from dialogue import *


class dialogue_thread(QThread):

	def __init__(self):
		QThread.__init__(self)
		self.voiceface = VoiceInterface()
		self.voiceface.hear_display = self.display
		self.voiceface.hear_voice = self.talk
		self.dialogue = DialogueManager(self.voiceface, DialogueModelTagging())

	def run(self):
		self.dialogue.run()
		return None

	def listen(self):
		YaoSpeech.listen()
		print "YaoSpeech: listening..."

	def recognize(self):
		result = YaoSpeech.recognize()
		if result == None or result == '':
			return
		result = result.decode('utf-8')
		print "speech recognized: ", result
		self.emit(QtCore.SIGNAL('display(QString, QString)'), u'Human: '+result, '#bb2244')
		self.voiceface.addMessage(result)
		print "YaoSpeech: recognizing..."

	def display(self, msg):
		self.emit(QtCore.SIGNAL('display(QString, QString)'), u'Machine: '+msg, '#00aa00')	

	def talk(self, msg):
		msg = msg.replace(u'\'', u'\\\'')
		msg = msg.replace(u'\n', u'\\\n')
		msg = msg.replace(u'\t', u'\n')
		print msg
		YaoSpeech.speak((u'\"'+msg+u'\"').encode('utf-8'))



def main():
    app = QtGui.QApplication(sys.argv)
    gui = GUI()	
    thread = QThread()
    dialogue = dialogue_thread()
    gui.connect(dialogue, QtCore.SIGNAL("display(QString, QString)"), gui.display)
    dialogue.connect(gui, QtCore.SIGNAL('listen()'), dialogue.listen)
    dialogue.connect(gui, QtCore.SIGNAL('recognize()'), dialogue.recognize)
    dialogue.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()