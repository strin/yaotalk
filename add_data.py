#!/usr/bin/env python
#coding:utf-8
from data import database, translate
import shelve
db = shelve.open('iiis-shelve')
db['db'] = database
db['translate'] = translate
db.close()

