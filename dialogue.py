# coding: utf-8
# %load_ext autoreload
# %autoreload 2

import random
import sys

import data
import jieba
import color
import time

from knowledge import *

import sys
import manager as dbman
import numpy

class VoiceInterface :
	def __init__(self) :
		self.msg_queue = list()

	def hear_display(self, message):
		return None

	def hear_voice(self, messaeg):
		return None

	def hear(self, message) :
		self.hear_display(message)
		self.hear_voice(message)

	def talk(self) :
		while len(self.msg_queue) == 0:
			time.sleep(0.05)	
		msg = self.msg_queue.pop()
		return msg

	def addMessage(self, msg):
		self.msg_queue.append(msg)


class StdoutInterface :
	def hear(self, message) :
		print 'M: '+message

	def talk(self) :
		return 'H: '+sys.stdin.readline()

class FixedFlowModel:
	def __init__(self):
		# self.queue = [u'帕帕的秋季学期课程如何？']
		# self.queue = [u'王立威的机器学习怎么样？']
		# self.queue = [u'王立威的课程']
		self.queue = [u'王立威这个老师怎么样？', u'课程吧', u'好的']
		# self.queue = [u'姚班', u'好的', u'对']
		# self.queue = [u'姚班 的 课程', u'徐佳']
		self.queue = [u'谁 是 姚期智']

	def hear(self, message):
		color.beginError()
		print 'M: '+str(message.encode('utf-8'))
		color.end()

	def talk(self) :
		if len(self.queue) == 0:
			return None
		msg = self.queue[0]
		color.beginTitle()
		print 'H: '+msg
		color.end()
		self.queue = self.queue[1:]
		return msg

class DialogueModelTagging:

	def __init__(self):
		self.manager = dbman.Manager()
		self.talk_count = 0

		# yes or no question.
		self.yes_keyword = None
		self.yes_prompt = None
		self.no_keyword = None
		self.yes_confirmation = [u'想',u'好', u'好的', u'嗯', u'可以', u'是', u'没问题', u'对', u'对的']
		self.no_confirmation = [u'不', u'不用', u'算了', u'不要']


	def talk_first(self):
		self.talk_count = self.talk_count+1
		msg_list = [u'你好！', u'你好，欢迎关注姚班！', u'你好，很高兴见到你。', u'你好，想了解关于姚班的什么方面',\
						 u'这里是交叉信息研究院，有什么需要帮助的吗？']
		coin = random.randint(0, len(msg_list)-1)
		return msg_list[coin]

	# output unicode.
	def talk(self):
		if self.talk_count == 0:
			return self.talk_first()
		return self.response

	def hit(self, keywords, tags):
		count = 0
		for word in keywords:
			for tag in tags:
				if word == tag:
					count = count+1
		return float(count)

	# take in unicode.
	def hear(self, message):
		keywords = message.split(u' ')
		# keywords = list(jieba.cut(message))
		keywords = [word for word in keywords if word != u' ']
		print 'keywords = ', keywords
		# answer yes/no question.
		if self.yes_keyword != None and self.hit(keywords, self.yes_confirmation) > 0:
			keywords = [self.yes_keyword]
			self.yes_prompt = None
			self.yes_keyword = None
		elif self.yes_prompt != None and self.hit(keywords, self.yes_confirmation) > 0:
			self.response = self.yes_prompt
			self.yes_prompt = None
			self.yes_keyword = None
			return None
		elif self.yes_keyword != None:
			self.response = u'那就算了吧'
			self.yes_prompt = None
			self.yes_keyword = None
			return None

		dic_list = self.manager.query(keywords)
		# print dic_list

		if dic_list == None or len(dic_list) == 0:
			self.response = self.noneResponse()
		responses = list()
		scores = list()
		max_score = 0
		max_response = None
		max_dic = None
		for dic in dic_list:
			scores.append(self.hit(keywords,dic['tag']))
			if dic.has_key('func'):
				func = dic['func']
				responses.append(func(dic))
			else:
				responses.append(self.noneResponse())
			if scores[len(scores)-1] > max_score:
				max_score = scores[len(scores)-1]
				max_response = responses[len(responses)-1]
				max_dic = dic
		dic = None
		if len(responses) != 0 and numpy.sum(scores) != 0:
			self.response = max_response
			dic = max_dic
			# scores = numpy.divide(scores, numpy.sum(scores))
			# coin = random.random()
			# score_sum = 0
			# print scores
			# for i in range(len(scores)):
			# 	score_sum = score_sum+scores[i]
			# 	if score_sum >= coin:
			# 		break
			# self.response = responses[i]
			# dic = dic_list[i]
		elif len(responses) != 0:
			self.response = responses[0]
		else:
			self.response = self.noneResponse()
		
		# ask.
		print dic
		if dic != None and dic.has_key(u'Q'):
			question = dic[u'Q'](dic)
			self.response = self.response+u'。'+question[u'str']
			self.yes_keyword = question[u'yes_keyword']
			self.yes_prompt = question[u'yes_prompt']
			self.no_keyword = question[u'no']


	# none response.
	def noneResponse(self):
		return u'不知道呀！'
		


class DialogueManager :
	''' initialize a dialogue between A and B 
	A, B should implement the following:
		hear(message).   
		message = talk().
	'''
	def __init__(self, personA = StdoutInterface(), personB = DialogueModelTagging()) :
		self.round = 0
		self.person = list()
		self.person.append(personA)
		self.person.append(personB)

	''' run the dialogue
		current implementation: by turn.
	'''
	def run(self) :
		coin = random.random()
		# round = int(coin > 0.5)
		round = 1
		while True:
			message = self.person[round].talk()
			if message == None:  
				break
			round = (round+1)% 2
			self.person[round].hear(message)
	

