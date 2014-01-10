# coding: utf-8

from knowledge import *


course = KDim(['课程','课'])
point_algo = KPoint(['算法','算法设计','算法分析'])
point_ml = KPoint(['机器学习', '人工智能'])
course.addPoint(point_algo)
course.addPoint(point_ml)

season = KDim(['学期','学期制'])

point_spring = KPoint(['春季学期'])
point_autumn = KPoint(['秋季学期'])
point_summer = KPoint(['夏季学期'])
season.addPoint(point_spring)
season.addPoint(point_summer)
season.addPoint(point_autumn)


teacher = KDim(['教授','老师','任课老师'])
point_lijian = KPoint(['李建'])
point_liwei = KPoint(['王立威','北大'])
teacher.addPoint(point_lijian)
teacher.addPoint(point_liwei)

field = KDim(['领域','学科','方向'])
point_field_algo = KPoint(['算法'])
point_field_crypto = KPoint(['语音'])
point_field_ml = KPoint(['机器学习'])
field.addPoint(point_field_ml)
field.addPoint(point_field_crypto)
field.addPoint(point_field_algo)

print field
print teacher
print course
print season
