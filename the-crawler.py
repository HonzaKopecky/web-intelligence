from lib.crawler import Crawler
from lib.indexer import Indexer

crawler = Crawler(3)

crawler.addSeed("https://hubpraha.cz/en")

crawler.crawl()

crawler.saveDocuments("out/documents")

indexer = Indexer()

indexer.indexDocs(crawler.documents)

indexer.printIndex()