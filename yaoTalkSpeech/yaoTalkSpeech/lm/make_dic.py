import jieba

# cmu = file('cmu.dic').readlines()
# cmu_dict = dict()
# for line in cmu:
# 	line = line.decode('utf-8')
# 	line = line[:len(line)-1]
# 	pos = line.find(u' ')
# 	keyword = line[:pos].lower()
# 	content = line[pos:].lower()
# 	cmu_dict[keyword] = content

chinese = file('zh_broadcastnews_utf8.dic').readlines()
chinese_dict = dict()
for line in chinese:
	line = line.decode('utf-8')
	line = line[:len(line)-1]
	pos = line.find(u' ')
	keyword = line[:pos].lower()
	content = line[pos:].lower()
	chinese_dict[keyword] = content

dic = file('user_ch.dic').readlines()
output = open('speech.dic', 'w')
word_dict = dict()

for line in dic:
	line = line.decode('utf-8')
	line = line.split(u' ')
	if word_dict.has_key(line[0]):  # duplication.
		continue
	else:
		word_dict[line[0]] = True
	if chinese_dict.has_key(line[0]):
		output.write((line[0]+chinese_dict[line[0]]+'\n').encode('utf-8'))
	elif line[0][0] >= u'\u4e00' and line[0][0] <=u'\u9fa5' : # is chinese
		words = list(jieba.cut(line[0]))
		res = list()
		for word in words:
			if chinese_dict.has_key(word):
				res.append(chinese_dict[word])
			else:
				res = None
				break
		if res != None:
			output.write((line[0]+' '.join(res)+'\n').encode('utf-8'))
		else:
			res = list()
			for uchar in line[0]:
				if chinese_dict.has_key(uchar):
					res.append(chinese_dict[uchar])
				else:
					res = None
					break

			if res != None:
				output.write((line[0]+' '.join(res)+'\n').encode('utf-8'))





output.close()