#!/opt/local/bin/python
# coding: utf-8

from dialogue import *
from data import *
from knowledge import *



manager = DialogueManager(FixedFlowModel(), DialogueModelTagging())
manager.run()


