from the_crawler import the_crawler
from the_indexer import prepare_index, load_documents
from boolean_search import boolean_search
from vector_search import vector_search

version = '0.1'

print("Welcome to Search Engine Example!")
print("Created by Jan Kopecký during Web Intelligence course at AAU (2018).\n")

while True:
    print("Available functions")
    print("\t1. Web crawler")
    print("\t2. Boolean search")
    print("\t3. Vector model search")
    op = input("\nSelect function [1,2,3]: ")
    if op not in ['1', '2', '3']:
        print("Invalid input.")
    else:
        if op == '1':
            the_crawler()
            quit(0)
        docs = load_documents()
        index = prepare_index(docs, op == '2')
        if op == '2':
            boolean_search(index, docs)
        else:
            vector_search(index, docs)
        quit(0)
