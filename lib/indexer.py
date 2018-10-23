import pickle
import math
from .tokensParser import TokensParser


class Indexer:
    def __init__(self):
        self.index = dict()
        self.parser = TokensParser()

    def index_docs(self, docs):
        for doc in docs:
            self.index_doc(doc)

    # get all tokens of the document and add their occurrence to the index
    # tokens are lowercase and stemmed
    # algorithm does not work with synonyms and homonyms in any way (car != automobile)
    def index_doc(self, document):
        tokens = self.parser.get_tokens(document.rawText)
        for token in tokens:
            self.add_occurrence(token, document)

    # add token occurrence into the index
    # inverted index is implemented so we have a dictionary of words
    # every word entry contains a list of documents that contain the word
    # occurrence count in that document is also stored
    def add_occurrence(self, word, doc):
        if word in self.index:
            if doc.id in self.index[word]['postings']:
                self.index[word]['postings'][doc.id] = self.index[word]['postings'][doc.id] + 1
            else:
                self.index[word]['postings'][doc.id] = 1
                self.index[word]['count'] = self.index[word]['count'] + 1
        else:
            # as long as we iterate over a list of documents sorted by ID
            # the inverted index for every word is sorted too
            self.index[word] = {'count' : 1, 'postings' : {doc.id : 1}}

    def save_index(self, path):
        f = open(path, "wb")
        pickle.dump(self.index, f)
        f.close()

    @staticmethod
    def load_index(path):
        f = open(path, "rb")
        index = pickle.load(f)
        return index

    @staticmethod
    def compute_tfidf_index(index, documents):
        for term in index:
            # print(term)
            index[term]['idf'] = Indexer.compute_idf(index[term]['count'], len(documents))
            # print("\t" + str(len(documents)) + "/" + str(index[term]['count']) + "=" + str(index[term]['idf']))
            for key in index[term]['postings']:
                index[term]['postings'][key] = Indexer.compute_tfidf(index[term]['idf'], index[term]['postings'][key])
                # print("\t\t" + str(key) + " : " + str(index[term]['postings'][key]))
        parser = TokensParser()
        for doc in documents:
            tokens = parser.get_tokens(doc.rawText)
            tokens = set(tokens)
            length = 0
            for token in tokens:
                length = length + math.pow(Indexer.compute_tfidf(index[token]['idf'], index[token]['postings'][doc.id]), 2)
            doc.score = math.sqrt(length)
        return index

    @staticmethod
    def compute_tfidf(idf, occurrence_count):
        tf = Indexer.compute_tf(occurrence_count)
        return tf * idf

    @staticmethod
    def compute_tf(occurrence_count):
        if occurrence_count == 0:
            return 0
        return 1 + math.log10(occurrence_count)

    @staticmethod
    def compute_idf(dft, n):
        return math.log10(n / dft)

    @staticmethod
    def compute_champions(index, r):
        for term in index:
            index[term]['champions'] = Indexer.get_champions(index[term], r)
        return index

    @staticmethod
    def get_champions(term, r):
        if len(term['postings']) <= r:
            return term['postings']
        postings = dict(term['postings'])
        champions = dict()
        for i in range(1, r):
            Indexer.add_next_champion(postings, champions)
        return champions

    @staticmethod
    def add_next_champion(postings, champions):
        max_score = None
        max_posting_key = None
        for i in postings:
            if max_score is None or postings[i] > max_score:
                max_posting_key = i
                max_score = postings[i]
        champions[max_posting_key] = postings[max_posting_key]
        postings.pop(max_posting_key,None)
