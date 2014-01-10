# coding: utf-8

from knowledge import *
from sys import *
# import sys
# sys.path.append('Fetcher/')
# import shelve
# shelve_db = shelve.open('Fetcher/iiis-shelve')


keys = ['老师', '课程', '学期', '领域', '学分', 'info']
values = [['帕帕', '算法设计', '秋季学期', '算法', 4, '本课程介绍算法设计的基础知识，常用算法设计技术，以及算法复杂性的分析。主要内容包括：算法分析工具，分治算法，动态规划，贪心算法等算法设计技巧，以及NP完全性，随机算法，近似算法等高级专题'],
		   ['唐平中','博弈论', '春季学期', '经济', 3, '本课程建议学生掌握线性代数基础知识及微积分基本技巧，但不是硬性要求。本课程拟介绍相关材料并培养学生的数学技巧。本课程是博弈论入门课程，拟从博弈论基础知识着手。课程将介绍纳什均衡等重要概念，旨在引导学生学习演化博弈论、博弈图等更为复杂的课题。'],  
		  ['王立威', '机器学习', '秋季学习', '数据', 4, '机器学习研究的内容是如何使计算机从经验中学习。通过结合理论计算机与统计学的思想，目前已开发出很多机器学习的算法，并成功应用于计算机视觉、生物信息学以及自然语言处理等多个领域。机器学习理论研究机器学习的根本问题，包括在什么条件下是可学习的，以及学习能力的理论极限是多少。'],
		  ['帕帕', KNS, KNE, KNE, KNE, '帕帕上课很有激情'],
		  ['王立威', KNS, KNE, KNE, KNE, '非常自High'],
		  ['王立威', KNE, KNE, KNE, KNE, 'IEEE AI\'s 10 to watch'],
		  [KNE, '博弈论', KNS, KNE, KNE, '']]

argmax = lambda array : max([[array[i],i] for i in range(len(array))])[1]

# give each piece in *values* a score
# if multiple pieces are hit by search, pick the piece with *smallest* score .
# if no piece is hit by search, pick the piece with *highest* score.
def scoring(piece):
	res = 0
	for item in piece:
		if item == KNE:
			res += 0
		elif item == KNS:
			res += 2
		else:
			res += 5
	return res

def scoring_hit(num_hit):
	return num_hit*10

def hit(a, keydict):
	for x in a:
		if keydict.has_key(x):
			return True
	return False

def search(keys, values, keywords):
	word_dict = dict()
	for word in keywords:
		word_dict[word] = True
	perfect_match = list()	
	partial_match = list()
	scores = list()
	for pi in range(len(values)):
		piece = values[pi]
		scores.append(scoring(piece))
		piece = piece[:len(piece)-1]
		# matching.
		satisfy_perfect = True
		satisfy_partial = False
		for index in range(len(piece)): # skipping info, which is always fixed.
			if hit([piece[index]], word_dict):
				satisfy_partial = True
				continue
			elif piece[index] == KNS and hit([keys[index]], word_dict):
				satisfy_partial = True
				continue
			elif piece[index] == KNE and (not hit([keys[index]], word_dict)):
				continue
			else:
				satisfy_perfect = False
		if satisfy_partial: # partial match.
			partial_match.append(pi)
		if satisfy_perfect: # perfect match.
			perfect_match.append(pi)
	print 'perfect match = ', perfect_match
	print 'partial match = ', partial_match
	if perfect_match != []:
		return min([[scores[i],values[i]] for i in perfect_match])[1]
	elif partial_match != []:
		return max([[scores[i],values[i]] for i in partial_match])[1]
	else:
		return None

query = ['帕帕']
res = search(keys, values, query)
stdout.write('query = ')
[stdout.write(x+' ') for x in query]
stdout.write('\n')
print 'res = ', res[len(res)-1]
# klg = Knowledge()
# data = shelve_db['老师']
# klg.buildFromTable(data)

