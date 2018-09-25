import lib.crawler

crawler = lib.crawler.Crawler(10)

crawler.addSeed("https://hubpraha.cz")

crawler.crawl()

print(crawler.documents)
# print(crawler.urlQueue.qsize())