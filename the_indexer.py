from lib.indexer import Indexer
from lib.crawler import Crawler


def load_documents():
    path = input("\nEnter the path to crawled documents: ")
    print("Loading documents...")
    docs = Crawler.load_documents(path)
    print("" + str(len(docs)) + " documents successfully loaded.")
    return docs


def prepare_index(docs, boolean=False):
    print("Generating term-document index...")
    indexer = Indexer()
    indexer.index_docs(docs)
    print("Computing TF-IDF* index...")
    tfidf_index = Indexer.compute_tfidf_index(indexer.index, docs)
    if boolean:
        return tfidf_index
    while True:
        limit = input("\nHow many champions would you like to generate for each term: ")
        try:
            if int(limit):
                break
        except:
            continue
    championed = Indexer.compute_champions(tfidf_index, int(limit))
    print("Index of " + str(len(championed)) + " terms successfully generated.")
    return championed
