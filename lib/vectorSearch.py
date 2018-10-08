from .tokensParser import TokensParser

class VectorSearch:
	def __init__(self, index):
		self.index = index

	def searchSimpleScore(self, query):
		docs = self.getDocs(query)
		result = self.countScores(docs)
		return self.orderResults(result)

	def getDocs(self, query):
		parser = TokensParser()
		tokens = parser.getTokens(query)
		docs = self.getPossibleDocs(tokens)
		return docs
		
	def getPossibleDocs(self, tokens):
		docs = dict()
		for token in tokens:
			if token not in self.index:
				continue
			print(self.index[token])
			for key in self.index[token]:
				if key in ["count","idf"]:
					continue
				if key not in docs:
					docs[key] = dict()
					docs[key]['id'] = key
					docs[key]['weights'] = [self.index[token][key]]
				else:
					docs[key]['id'] = key
					docs[key]['weights'].append(self.index[token][key])
		return docs

	@staticmethod
	def countScores(docs):
		for key in docs:
			finalWeight = 0
			for weight in docs[key]['weights']:
				finalWeight += weight
			docs[key]['finalWeight'] = finalWeight
		return docs

	@staticmethod
	def orderResults(docs):
		result = list()
		while len(docs) > 0:
			max = VectorSearch.getMaxDoc(docs)
			result.append(max['id'])
			docs.pop(max['id'],None)
		return result

	@staticmethod
	def getMaxDoc(docs):
		maxScore = None
		maxDoc = None
		for key in docs:
			if maxScore is None or docs[key]['finalWeight'] > maxScore:
				maxDoc = docs[key]
				maxScore = docs[key]['finalWeight']
		return maxDoc



