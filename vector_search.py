from lib.vectorSearch import VectorSearch
from lib.pageRank import PageRank


def vector_search(index, documents):
    while True:
        use_rank = input("\nUse PageRank [yes/no]? ")
        if use_rank in ['yes', 'no']:
            break
    if use_rank == 'yes':
        documents = prepare_ranking(documents)
    se = VectorSearch(index, documents)
    do_search(se)


def do_search(se):
    while True:
        query = input("\nEnter query: ")
        use_champions = input("Do you want to use champions?[yes/no]: ")
        use_champions = True if (use_champions == 'yes' or use_champions == '') else False
        result = se.search_vector(query, use_champions)
        for i in range(0, 9 if len(result) >= 10 else len(result)):
            print(se.docs[result[i]].url)


def prepare_ranking(docs):
    while True:
        alpha = input("\nRandom surfer probability (0.1 - 0.9): ")
        try:
            if float(alpha):
                break
        except:
            continue
    while True:
        threshold = input("\nPageRank difference threshold (0.00001 - 0.001): ")
        try:
            if float(threshold):
                break
        except:
            continue
    pr = PageRank(docs, float(alpha), float(threshold))
    print("Ranking documents...")
    docs = pr.rank_documents()
    print("Documents ranked.")
    return docs
