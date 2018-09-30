import lib.crawler

crawler = lib.crawler.Crawler(10)

crawler.addSeed("https://hubpraha.cz")

crawler.crawl()

crawler.saveDocuments("out/documents")
# print(crawler.urlQueue.qsize())