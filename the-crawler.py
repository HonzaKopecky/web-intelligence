from lib.crawler import Crawler
from lib.indexer import Indexer
from lib.booleanSearch import BooleanSearch

# Crawl specified ammount of pages and save them to a file.
# crawler = Crawler(200)
# crawler.addSeed("https://hubpraha.cz/en")
# crawler.crawl()
# crawler.saveDocuments("out/documents")

# Generate index from crawled documents stored in a file and save it to a file
# indexer = Indexer()
# indexer.indexDocs(Crawler.loadDocuments("out/documents"))
# indexer.saveIndex("out/index")

# Load pre-built index and pre-crawled documents to perform search over them
documents = Crawler.loadDocuments("out/documents")
index = Indexer.loadIndex("out/index")

search = BooleanSearch(index, documents)

print(
	search.b_and(
		search.b_and(
			search.b_term("hub"),
			search.b_term("praha")
		),
		search.b_not(
			search.b_term("impact")
		)
	)
)