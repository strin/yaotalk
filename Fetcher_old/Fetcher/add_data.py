#!/usr/bin/env python
# coding: utf-8
from initdata import professors, courses, history, target, constitute, info
import shelve
db = shelve.open('iiis-shelve')
db['教授'] = professors
db['老师'] = professors
db['课程'] = courses
db['历史'] = history
db['目标'] = target
db['机构'] = constitute
db['info'] = info
db.close()

