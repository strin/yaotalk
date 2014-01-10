
dic = file('user.dict').readlines()
output = open('user_ch.dic', 'w')
word_dict = dict()

for line in dic:
	line = line.decode('utf-8')
	line = line.split(u' ')
	if word_dict.has_key(line[0]):  # duplication.
		continue
	elif line[0][0] >= u'\u4e00' and line[0][0] <=u'\u9fa5' : # is chinese
		word_dict[line[0]] = True
		output.write((line[0]+' %s'%line[1]).encode('utf-8'))
output.close()