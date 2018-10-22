from lib.crawler import Crawler
from lib.indexer import Indexer
from lib.booleanSearch import BooleanSearch
from lib.vectorSearch import VectorSearch
from lib.document import Document

def doSearch(se):
	while True:
		query = input("Enter query: ")
		result = se.searchVector(query);
		for i in result:
			print(se.docs[i].url);

#Crawl specified ammount of pages and save them to a file.
# crawler = Crawler(1000)
# crawler.addSeed("https://www.hubpraha.cz/en")
# crawler.addSeed("https://www.hubbrno.cz/en")
# crawler.addSeed("https://www.en.aau.dk/")
# crawler.crawl()
# crawler.saveDocuments("out/1000documents-v2")

documents = Crawler.loadDocuments("out/1000documents")

# search = BooleanSearch(index, documents)
# print(
# 	search.b_and(
# 		search.b_and(
# 			search.b_term("hub"),
# 			search.b_term("praha")
# 		),
# 		search.b_not(
# 			search.b_term("impact")
# 		)
# 	)
# )

# Generate index from crawled documents stored in a file and save it to a file
indexer = Indexer()
indexer.indexDocs(documents)

index = indexer.index
TFIDFindex = Indexer.computeTFIDFIndex(index, documents)

championed = Indexer.computeChampions(TFIDFindex, 10)
print(championed['praha']['champions'])

vectorS = VectorSearch(TFIDFindex, documents)
doSearch(vectorS)

#20:34 start 1000 docs