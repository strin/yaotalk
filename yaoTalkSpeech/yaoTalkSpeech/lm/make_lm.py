# coding: utf8
dic = file('user_ch.dic').readlines()
output = open('lm_prepare.txt', 'w')
word_dict = dict()


for line in dic:
	line = line.decode('utf-8')
	line = line.split(u' ')
	occur = int(line[1])
	if word_dict.has_key(line[0]):  # duplication.
		continue
	else:
		word_dict[line[0]] = True
	if len(line[0]) >= 8:
		continue
	for i in range(occur):
		output.write(line[0].encode('utf-8')+'\n')
output.close()