from .tokensParser import TokensParser
from .indexer import Indexer

class VectorSearch:
	def __init__(self, index, docs):
		self.index = index
		self.docs = docs

	def searchSimpleScore(self, query):
		docs = self.getDocs(query)
		result = self.countScores(docs)
		return self.orderResults(result)

	def searchVector(self, query):
		docs = self.getDocs(query)
		print("Possible documents:")
		print(docs)
		queryVector = self.getQueryVector(query)
		print("Query vector:")
		print(queryVector)	
		result = VectorSearch.countCosineScores(docs, queryVector)
		print(result)
		result = VectorSearch.orderResults(result)
		return result


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
			for key in self.index[token]['postings']:
				if key not in docs:
					docs[key] = dict()
				docs[key]['id'] = key
				if not 'tokens' in docs[key]:
					docs[key]['tokens'] = dict()
				docs[key]['tokens'][token] = self.index[token]['postings'][key]
				docs[key]['score'] = self.docs[key].score
		return docs

	@staticmethod
	def countScores(docs):
		for key in docs:
			score = 0
			for token in docs[key]['tokens']:
				score += docs[key]['tokens'][token]
			docs[key]['score'] = score
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
			if maxScore is None or docs[key]['score'] > maxScore:
				maxDoc = docs[key]
				maxScore = docs[key]['score']
		return maxDoc

	def getQueryVector(self, query):
		parser = TokensParser()
		tokens = parser.getTokens(query)
		vector = dict()
		for token in tokens:
			if not token in self.index:
				continue
			print(self.index[token])
			vector[token] = Indexer.computeTFIDF(self.index[token]['idf'],1)
		return vector

	@staticmethod
	def countCosineScores(docs, queryVector):
		for doc in docs:
			cosineScore = 0
			for token in docs[doc]['tokens']:
				cosineScore = cosineScore + ((queryVector[token] * docs[doc]['tokens'][token]) / docs[doc]['score'])	
			docs[doc]['score'] = cosineScore
		return docs

