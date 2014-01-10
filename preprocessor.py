# coding: utf-8

import argparse
import os
from HTMLParser import HTMLParser
import lxml
import jieba
import jieba.analyse
from lxml.html.clean import Cleaner

# strip off html tags.
def processDir(data_dir, output_dir):
	if not os.path.exists(output_dir):
	    os.makedirs(output_dir)

	# process every html document.
	file_list = os.listdir(data_dir);
	html_cleaner = Cleaner()
	html_cleaner.javascript = True
	html_cleaner.style = True
	word_dict = dict()
	def updateWordDict(word):
		if word_dict.has_key(word):
			word_dict[word] = word_dict[word]+1  
		else:
			word_dict[word] = 1
	for file_name in file_list:
		if file_name[0] == '.':
			continue
		# remove html tags.
		parsetree = lxml.html.parse(data_dir+'/'+file_name)
		parsetree = html_cleaner.clean_html(parsetree)
		content = parsetree.getroot().text_content()

		# word extraction.
		words_raw = list(jieba.cut(content))
		words = list()
		for word in words_raw:
			uchar = word[0]
			if uchar >= u'\u4e00' and uchar<=u'\u9fa5' : # chinese.
				words.append(word)
				updateWordDict(word)
			if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
				word = word.lower()
				words.append(word)
				updateWordDict(word)
		# print words
		text  = ' '.join(words)
		# print text
		output = open(output_dir+file_name, 'w')
		output.write(text.encode('utf-8'))
		output.close()
	output = open(output_dir+'words.dict', 'w')
	for word in word_dict.keys():
		output.write(word.encode('utf-8')+' '+str(word_dict[word])+'\n')


processDir('./result/', './result_plain/')