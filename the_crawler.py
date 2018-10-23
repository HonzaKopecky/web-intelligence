from lib.crawler import Crawler

from lib.vectorSearch import VectorSearch
from lib.document import Document
from lib.pageRank import PageRank


def the_crawler():
    while True:
        limit = input("Enter the number of documents that you want to fetch: ")
        try:
            if int(limit):
                break
        except:
            continue
    crawler = Crawler(int(limit))
    while True:
        seed = input("Add seed URL (enter q to stop adding): ")
        if seed == "q":
            break
        crawler.add_seed(seed)
    print("\nCrawling of " + str(limit) + " files started.")
    crawler.crawl()
    print("\nCrawling finished. " + str(len(crawler.documents)) + " documents crawled.")
    path = input("Enter path to a file where you want to store the crawled documents: ")
    crawler.save_documents(path)
    print("\nDocuments stored. Good bye!")
