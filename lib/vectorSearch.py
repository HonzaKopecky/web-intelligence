from .tokensParser import TokensParser
from .indexer import Indexer


class VectorSearch:
    def __init__(self, index, docs):
        self.index = index
        self.docs = docs

    def search_simple_score(self, query):
        docs = self.get_docs(query, False)
        result = self.count_scores(docs)
        return self.order_results(result)

    def search_vector(self, query, champions=False):
        docs = self.get_docs(query, champions)
        # print("Possible documents:")
        # print(docs)
        query_vector = self.get_query_vector(query)
        # print("Query vector:")
        # print(queryVector)
        docs_scored = VectorSearch.count_cosine_scores(docs, query_vector)
        docs_ranked = self.apply_page_rank(docs_scored)
        # print(result)
        result = VectorSearch.order_results(docs_ranked)
        return result

    def get_docs(self, query, use_champions):
        parser = TokensParser()
        tokens = parser.get_tokens(query)
        docs = self.get_possible_docs(tokens, use_champions)
        return docs

    def get_possible_docs(self, tokens, use_champions):
        docs = dict()
        for token in tokens:
            if token not in self.index:
                continue
            candidates = self.index[token]['champions'] if use_champions else self.index[token]['postings']
            for key in candidates:
                if key not in docs:
                    docs[key] = dict()
                docs[key]['id'] = key
                if 'tokens' not in docs[key]:
                    docs[key]['tokens'] = dict()
                docs[key]['tokens'][token] = candidates[key]
                docs[key]['score'] = self.docs[key].score
        return docs

    @staticmethod
    def count_scores(docs):
        for key in docs:
            score = 0
            for token in docs[key]['tokens']:
                score += docs[key]['tokens'][token]
            docs[key]['score'] = score
        return docs

    @staticmethod
    def order_results(docs):
        result = list()
        while len(docs) > 0:
            max_doc = VectorSearch.get_max_doc(docs)
            result.append(max_doc['id'])
            docs.pop(max_doc['id'], None)
        return result

    @staticmethod
    def get_max_doc(docs):
        max_score = None
        max_doc = None
        for key in docs:
            if max_score is None or docs[key]['ranked_score'] > max_score:
                max_doc = docs[key]
                max_score = docs[key]['ranked_score']
        return max_doc

    def get_query_vector(self, query):
        parser = TokensParser()
        tokens = parser.get_tokens(query)
        vector = dict()
        for token in tokens:
            if token not in self.index:
                continue
            # print(self.index[token])
            vector[token] = Indexer.compute_tfidf(self.index[token]['idf'], 1)
        return vector

    @staticmethod
    def count_cosine_scores(docs, query_vector):
        for doc in docs:
            cosine_score = 0
            for token in docs[doc]['tokens']:
                cosine_score = cosine_score + ((query_vector[token] * docs[doc]['tokens'][token]) / docs[doc]['score'])
            docs[doc]['score'] = cosine_score
        return docs

    # cosine score is simply multiplied with page rank
    # there are some more advanced techniques to combine page rank and content based search
    # the ones that I saw are using tfidf and page rank to rank all pages at query time
    def apply_page_rank(self, results):
        for key in results:
            results[key]['ranked_score'] = results[key]['score'] * self.docs[key].page_rank
            # print(str(results[key]['score']) + '->' + str(results[key]['ranked_score']))
        return results

