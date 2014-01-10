# coding: utf-8
# knowledg point, defines instantiations of properties such as [course] Algorithm Design, Machine Learning, etc.

# class KLabel:
# 	def __init__(self, _name):
# 		self.name = _name
# 	def __str__(self):
# 		return self.name

# try KNS:
# except NameError:
# 	KNS = KLabel('[Not Specified]')

# try KNE:
# except NameError:
# 	KNE = KLabel('[Not Existed]')

KNS = 1
KNE = 0

''' return dim indices that have been filled 
'''
def retrieveActiveClass(piece):
	dim = list()
	for ind in range(len(piece)):
		if piece[ind] != KNE:
			dim.append(ind)
	return dim

''' decide if piecea is more general than pieceb 
'''
def knowledgePrec(piecea, pieceb):
	if len(piecea) != len(pieceb):
		return None
	index = list()
	for ind in range(len(piecea)):
		if piecea[ind] == pieceb[ind]:
			continue
		elif piecea[ind] == KNS and type(pieceb[ind]) == unicode:
			index.append(ind)
		elif piecea[ind] == KNE:
			index.append(ind)
		else:
			# print piecea[ind] == KNE, ' ', pieceb[ind]
			return None
	return index

''' decide if two knowledge pieces are equivalent 
'''
def knowledgeEqual(piecea, pieceb):
	return (knowledgePrec(piecea, pieceb) != None) & (knowledgePrec(pieceb, piecea) != None)

class KPoint:
	def __init__(self, _keywords = [""]):
		# variables.
		self.keywords = list(_keywords)
		self.dim = None

	def __str__(self):
		res = '-- point: '
		for word in self.keywords:
			res += word+' '
		return res


# knowldge dimension, defines properties such as courses, teachers, goals. 
class KDim:
	def __init__(self, _keywords = [""]):
		# variables.
		self.keywords = list(_keywords)
		self.points = []

	# add an instance to the property.
	def addPoint(self, _point):
		self.points.append(_point)
		_point.dim = self

	def __str__(self):
		res = '-- dim: '
		for word in self.keywords:
			res += word+' '
		res += '\n'
		for point in self.points:
			res += '\t'+str(point)+'\n'
		return res


# knowledge piece, defines a piece of information in the granularity tree.
class KPiece:
	def __init__(self):
		# state.
		self.kdims = []
		self.kpoints = []
		self.kdims_left = []
		
		# information in the piece.
		self.information = None

# knowledge tree.
class Knowledge:

	def __init__(self):
		self.root = KPiece()
		self.ktable = dict() # Kdim: Kpoint
		self.kdims = []
	# a table should be a list of dictionaries. 
	def buildFromTable(self, data):
		for key in data[0].keys():
			kdim = KDim([key])	# TODO: keywords.
			self.kdims.append(kdim) 
			for item in data[key]:
				print item







		
# # the Knowledge Granualrity Tree.
# class Knowledge:
# 	# Variables.  

