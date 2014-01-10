#!/opt/local/bin/python
# coding: utf-8

from dialogue import *
from data import *
from knowledge import *

manager = DialogueManager(FixedFlowModel(), DialogueModel())
manager.run()

# print knowledgeEqual(db_values[1][:len(db_keys)-1], db_values[1][:len(db_keys)-1])


