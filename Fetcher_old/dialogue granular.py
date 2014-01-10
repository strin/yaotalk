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

	def hear(self, message) :
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

class DialogueModel :

	def __init__(self, ) :
		# setting.
		self.dict_path = 'dict/user.dict'
		self.talk_count = 0

		# language. 
		self.last_msg = None
		self.last_response = None
		self.keyword_dict = None
		color.beginComment()
		jieba.load_userdict(self.dict_path)
		color.end()

		# state.
		self.state_key = None
		self.state_piece = None
		self.active_class = None
		self.active_piece = None
		self.state_vspecific = None # more specific peieces than *state_piece*
		self.state_vspecific_extra = None # which categories have such more specific info.
		self.current_db = None
		self.dim = 0
		self.dialogue_color = color.pcolors.ENDC

		# handle yes/no question.
		self.yesno_list = list()

	''' returns all pieces that are more specific than piece 
	'''
	def query_db(self, piece):
		res = list()
		for value in current_db:
			thispiece = value[self.dim]
			if knowledgePrec(piece, thispiece) != None:
				res.append(thispiece)
		return res

	def hear(self, message) :
		self.last_msg = message

	def talk_first(self):
		self.talk_count = self.talk_count+1
		msg_list = [u'你好！', u'你好，欢迎关注姚班！', u'你好，很高兴见到你。', u'你好，想了解关于姚班的什么方面',\
						 u'这里是交叉信息研究院，有什么需要帮助的吗？']
		coin = random.randint(0, len(msg_list)-1)
		return msg_list[coin]

	def talk(self):
		if self.talk_count == 0:
			return self.talk_first()
		last_response = ''
		# natural language understanding.
		if self.last_msg == None: return None
		color.beginComment()
		keywords = list(jieba.cut(self.last_msg))
		# self.display(keywords)
		color.end()
		self.buildKeywordDict(keywords)

		if self.classifyYesNo() and len(self.yesno_list) > 0:
			keywords = keywords+self.yesno_list
			self.buildKeywordDict(keywords)
			self.yesno_list = []
		# print self.yesno_list

		if self.active_class != None: 
			# downward search.
			values = [self.current_db[ind] for ind in self.active_piece]
			self.state_vspecific = None

			# upward search.

		else:	# rebuild.
			# knoledge acquisition.
			(keys, values) = data.search(data.db_keys, data.db_values, keywords)
			self.active_piece = range(len(values))
			self.state_key = keys
			self.current_db = values
			self.dim = len(self.state_key)-1
			values = self.current_db

		# produce output.
		# print values
		piece = self.answer(values)
		if piece != None:
			last_response = last_response+piece
		question = self.ask()
		if question != None:
			last_response = last_response+'\n'+question

		return last_response
	

	''' give each piece in *values* a score
		1. more specific, lower the score.
		2. higher the dim of piece, lower the score.
	'''
	def scoring(self, piece):
		res = 0
		for item in piece:
			if item == KNE:
				res += 0
			elif item == KNS:
				res += -2
			else:
				res += -5
		return res

	def hit(self, a):
		if type(a) != list:
			a = [a]
		for x in a:
			if self.keyword_dict.has_key(x):
				return True
		return False

	def buildKeywordDict(self, keywords):
		self.keyword_dict = dict()
		for word in keywords:
			self.keyword_dict[word] = True

	def classifyYesNo(self):
		if self.hit([u'好的',u'是的', u'好', u'是', u'可以', u'不错', u'yes']):
			return True
		elif self.hit([u'不', u'不用', u'算了', u'no']):
			return False
		else:
			return None

	def answer(self, values):
		keys = self.state_key
		scores = list()
		# print values
		for piece in values:
			hit_score = 0
			piece = piece[:len(piece)-1]
			for index in range(len(piece)):
				if self.hit([piece[index]]):
					hit_score = hit_score+50
				if piece[index] == KNS and self.hit([keys[index]]):
					hit_score = hit_score+25
				# if piece[index] == KNE and (not self.hit([keys[index]])) \
				# 	and (not self.hit([piece[index]])):
				# 	hit_score = hit_score+2
			# self.display(piece)
			# print 'score = ', hit_score+self.scoring(piece)
			scores.append(hit_score+self.scoring(piece))

		self.state_piece = max([[scores[i],values[i]] for i in range(len(values))])[1]
		info = self.state_piece[self.dim]
		self.state_piece = self.state_piece[:self.dim]
		self.active_class = retrieveActiveClass(self.state_piece)

		# filter out more specific peices.
		self.state_vspecific = list()
		self.state_vspecific_extra = list()
		active_piece = list()
		for ind in range(len(values)):
			piece = values[ind]
			piece = piece[:len(piece)-1]
			temp = knowledgePrec(self.state_piece, piece)
			if temp != None and knowledgePrec(piece, self.state_piece) == None: # strictly more specific.
				# print piece
				self.state_vspecific.append(piece)
				self.state_vspecific_extra.append(temp)
				active_piece.append(self.active_piece[ind])
		self.active_piece = active_piece
		return info
	
	''' plan an ask strategy.
	'''
	def ask(self):
		text = ''
		if self.state_piece == None:
			return None
		# looking for more specific information.
		for ind in range(self.dim):
			item = self.state_piece[ind]
			if item == KNS:
				candidate = set()
				for piece in self.state_vspecific:
					if piece[ind] != KNS and piece[ind] != KNE:
						candidate = candidate.union([piece[ind]])
				if len(candidate) == 1:
					text = self.state_key[ind]+u'中有'+candidate.pop()+u'。'
					text = text+u'想具体了解一下吗？'
					return text
				elif len(candidate) > 1:
					text = self.state_key[ind]+u'具体有'
					for x in candidate:
						text = text+x+' '
					text = text+u'想具体了解哪一个呢？'
					return text

		# extend the categories. (look for extra KNS)
		maxscore = sys.float_info.max
		maxind = None
		for ind in range(len(self.state_vspecific)):
			piece = self.state_vspecific[ind][:self.dim]
			if knowledgeEqual(piece, self.state_piece):
				continue
			score = self.scoring(piece)
			# print 'piece = ', score
			# print piece
			if score < maxscore:
				maxscore = score
				maxind = ind

		if maxind != None:
			text = u'想了解相关的方面吗？比如 '
			for i in range(len(self.state_vspecific_extra[maxind])):
				ind = self.state_vspecific_extra[maxind][i]
				text = text+self.state_key[ind]
				if i == len(self.state_vspecific_extra[maxind])-1:
					text = text+u'？'
				elif i == len(self.state_vspecific_extra[maxind])-2:
					text = text+u'或'
				else:
					text = text+u'、'
			
			return text

		return None
		
	# ''' generate the ask strategy to text 
	# '''
	# def ask_text(self, expect):
	# 	text = ''
	# 	# fill in state columns.
	# 	for ind in range(self.dim):
	# 		if self.state_piece[ind] == KNS:
	# 			newpiece = list(state_piece)


	# 	# explore new columns.
	# 	ind_kns = list()
	# 	ind_str = list()
	# 	for ind in expect:
	# 		if state_piece[ind] == KNS:
	# 			ind_kns.append(ind)
	# 		if type(state_piece[ind]) == unicode:
	# 			ind_str.append(ind)

	# 	if len(ind_kns) > 0:
	# 		text = u'你还想知道有关的其它信息吗？ 比如 '
	# 		for ind in ind_kns:
	# 			text = test+self.state_key[ind]+' '
	# 		text = text+u'?'



	# 	return None

	def display(self, lst) :
		for x in lst:
			sys.stdout.write('%s '%x)
		sys.stdout.write('\n')
		


class DialogueManager :
	''' initialize a dialogue between A and B 
	A, B should implement the following:
		hear(message).   
		message = talk().
	'''
	def __init__(self, personA = StdoutInterface(), personB = DialogueModel()) :
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
	

