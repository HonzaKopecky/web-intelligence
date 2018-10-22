import pickle, math

from .tokensParser import TokensParser

class Indexer:
	def __init__(self):
		self.index = dict()
		self.parser = TokensParser()

	def indexDocs(self, docs):
		for doc in docs:
			self.indexDoc(doc)

	#get all tokens of the document and add their occurence to the index
	#tokens are lowercased and stemmed
	#algorithm does not work with synonyms and homonyms in any way (car != automobile)
	def indexDoc(self, document):
		tokens = self.parser.getTokens(document.rawText)
		for token in tokens:
			self.addOccurence(token, document)

	#add token occurence into the index
	#inverted index is implemented so we have a dictionary of words
	#every word entry contains a list of documents that contain the word
	#occurence count in that document is also stored
	def addOccurence(self, word, doc):
		if word in self.index:
			if doc.id in self.index[word]['postings']:
				self.index[word]['postings'][doc.id] = self.index[word]['postings'][doc.id] + 1
			else:
				self.index[word]['postings'][doc.id] = 1
				self.index[word]['count'] = self.index[word]['count'] + 1
		else:
			#as long as we iterate over a list of documents sorted by ID
			#the inverted index for every word is sorted too
			self.index[word] = {'count' : 1, 'postings' : {doc.id : 1}}

	def saveIndex(self, path):
		f = open(path, "wb")
		pickle.dump(self.index, f)
		f.close()

	@staticmethod
	def loadIndex(path):
		f = open(path, "rb")
		index = pickle.load(f)
		return index

	@staticmethod
	def computeTFIDFIndex(index, documents):
		for term in index:
			# print(term)
			index[term]['idf'] = Indexer.computeIDF(index[term]['count'], len(documents))
			# print("\t" + str(len(documents)) + "/" + str(index[term]['count']) + "=" + str(index[term]['idf']))
			for key in index[term]['postings']:
				index[term]['postings'][key] = Indexer.computeTFIDF(index[term]['idf'], index[term]['postings'][key])
				# print("\t\t" + str(key) + " : " + str(index[term]['postings'][key]))
		parser = TokensParser()
		for doc in documents:
			tokens = parser.getTokens(doc.rawText)
			tokens = set(tokens)
			length = 0
			for token in tokens:
				length = length + math.pow(Indexer.computeTFIDF(index[token]['idf'], index[token]['postings'][doc.id]),2)
			doc.score = math.sqrt(length)
		return index

	@staticmethod
	def computeTFIDF(idf, occurenceCount):
		tf = Indexer.computeTF(occurenceCount)
		return tf * idf

	@staticmethod
	def computeTF(occurenceCount):
		if occurenceCount == 0:
			return 0
		return 1 + math.log10(occurenceCount)

	@staticmethod
	def computeIDF(dft, n):
		return math.log10(n / dft)

	@staticmethod
	def computeChampions(index, r):
		for term in index:
			index[term]['champions'] = Indexer.getChampions(index[term], r)
		return index

	@staticmethod
	def getChampions(term, r):
		if len(term['postings']) <= r:
			return term['postings']
		postings = dict(term['postings'])
		champions = dict()
		for i in range(1, r):
			Indexer.addNextChampion(postings, champions)
		return champions

	@staticmethod
	def addNextChampion(postings, champions):
		maxScore = None
		maxPostingKey = None
		for i in postings:
			if maxScore is None or postings[i] > maxScore:
				maxPostingKey = i
				maxScore = postings[i]
		champions[maxPostingKey] = postings[maxPostingKey]
		postings.pop(maxPostingKey,None)
		