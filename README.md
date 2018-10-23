# Web search engine for Web Intelligence course at AAU

This is my solution of project work of Web Inteligence course at Aalborg University.

Project implements simple web search engine that consists of 3 main components: **crawler, indexer and vector search model.**

All the important implementation stuff can be found in lib directory. Files in the root directory
only implement user interface.

**So far you can find the following features implemented:**

* Crawler logic that downloads webpages stored in queue
* HTML document parser that extracts all the URLs from HTML document
* HTML document parser that strips all HTML from document and stores just the pure text
* robots.txt parser implemented using urllib.robotsparser library
* Tokens are stemmed using NLTK Snowball stemmer, stop words and punctuation is removed.
* Indexer logic that builds the TF-IDF* index with champions lists
* Boolean Search Model based on stacking functions that return result lists
* Vector Search Model based on cosine similarity between query and documents
* PageRank computing engine
* Vector Search Model based on TF-IDF* index and PageRank
