class BooleanSearch:
	def __init__(self, index, documents):
		self.index = index
		self.documents = documents

	def b_and(self, left, right):
		# This is effective thanks to the fact that left and right are sorted
		intersection = [x for x in left if x in right]
		return intersection

	def b_or(self, left, right):
		union = list(set().union(left,right))
		return union

	def b_not(self, unwanted):
		result = list()
		# Locate all documents that are not in the unwanted list
		# This would be highly ineficient in real environment - result 
		# list would have billions of entries
		for i in range(0, len(self.documents)):
			if i not in unwanted:
				result.append(i)
		return result

	def b_term(self, word):
		if word not in self.index:
			return []
		res = dict(self.index[word])
		res.pop('count',None)
		return res

	# def search(self, query):
	# 	qTerms = self.parseQuery(query)
	# 	return self.resolveQuery(qTerms)

	# def parseQuery(self, q):
	# 	words = q.split()
	# 	query = list()
	# 	for word in words:
	# 		i = len(query)
	# 		query.append(self.generateTerm(word, i, query))
	# 	return query

	# def generateTerm(self, word, i, query):
	# 	if word == "AND":
	# 		return query.append(BooleanAnd(query, i))
	# 	if word == "OR":
	# 		return query.append(BooleanOr(query, i))
	# 	if word == "NOT":
	# 		return query.append(BooleanNot(query, i))
	# 	return BooleanTerm(query, i, word)

	# def resolveQuery(self, q):
	# 	i = 0
	# 	while(len(q) > 1):
	# 		q = q[i].resolve(self.index)
	# 		i = (i + 1) % len(q)
	# 	res = q[0].resolve(self.index)
	# 	return res[0].getResult()

# I do no longer parse string query so I did not finish this part
class BooleanTerm:
	def __init__(self, query, pos, word = None, result = None):
		print("new term")
		self.query = query
		self.pos = pos
		self.word = word
		self.result = result

	def resolve(self, index):
		print("resolveTerm")
		res = index[self.word]
		res.pop('count',None)
		return self.rebuildQuery(res)

	def rebuildQuery(self, result):
		print("rebuild")
		newQuery = list()
		for i in range(0, self.getPrevious()):
			newQuery.append(self.query[i])
		newQuery.append(BooleanTerm(newQuery, self.getPrevious() + 1, None, result))
		for i in range(self.getNext(),len(self.query)):
			newQuery.append(self.query[i])
		return newQuery

	def getResult(self):
		return self.result

	def getPrevious(self):
		return self.pos - 1

	def getNext(self):
		return self.pos + 1

class BooleanAnd(BooleanTerm):
	def resolve(self, index):
		left = self.query[self.pos - 1].getResult()
		right = self.query[self.pos + 1].getResult()
		intersection = [x for x in left if x in right]


class BooleanOr(BooleanTerm):
	def getResult(self, index):
		left = self.query[self.pos - 1].getResult()
		right = self.query[self.pos + 1].getResult()
		union = list(set().union(left,right))
		return union

class BooleanNot(BooleanTerm):
	def getResult(self, index):
		right = self.query[self.pos + 1].getResult()
		result = list()
		for i in len(self.documents):
			if i not in right:
				result.append(i)
		return result