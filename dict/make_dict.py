# coding: utf-8

defined = file('define.dict').readlines()
output = open('user.dict', 'w')
for line in defined:
	line = line.replace(' ', '')
	output.write(line[:len(line)-1]+' 20'+'\n')

crawled = file('crawled.dict').readlines()
for line in crawled:
	output.write(line)

output.close()
