from nltk.stem.snowball import SnowballStemmer

class TokensParser:
	def __init__(self):
		self.index = dict()
		self.stemmer = SnowballStemmer("english")
		self.stops = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", 
		"your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", 
		"her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", 
		"themselves", "what", "which", "who", "whom", "this", "that", "these", "those", 
		"am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", 
		"having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", 
		"because", "as", "until", "while", "of", "at", "by", "for", "with", "about", 
		"against", "between", "into", "through", "during", "before", "after", "above", 
		"below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", 
		"again", "further", "then", "once", "here", "there", "when", "where", "why", "how", 
		"all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", 
		"nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", 
		"will", "just", "don", "should", "now"]

	#tokens are generated from the raw text by splitting by space characters 
	def getTokens(self, text):
		words = text.split()
		#words are filtered by removing stop words and stemming
		tokens = self.filterWords(words)
		return tokens

	#keep the word only in case it is not a stop word
	#stop words usually do not carry any meaning so it is good idea to ignore them
	#it actually reduces the size of index by 30-40%
	#it may cause harm in some cases - "King of England", etc.
	#after this filtering, stem the tokens
	def filterWords(self, words):
		out = list()
		for word in words:
			if not word in self.stops:
				#stem the word before inserting it into the list
				#words are also converted to lowercase partially to reduce size of the index
				#and partially because the users usually do not enter correct capitalization
				#when entering a search query
				out.append(self.stem(word).lower())
		return out

	#using NLTK Snowball stemmer for English
	#stemmer cuts prefixes and postfixes of the words and leaves just the roots
	#thanks to that size of the index is reduced and the search performance is improved
	def stem(self, word):
		return self.stemmer.stem(word)