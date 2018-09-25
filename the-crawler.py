import lib.crawler

crawler = lib.crawler.Crawler(10)

crawler.addSeed("http://rotterdam.impacthub.net/")

crawler.crawl()

print(crawler.documents)
# print(crawler.urlQueue.qsize())