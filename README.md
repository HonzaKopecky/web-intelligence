# Web search engine for Web Intelligence course at AAU

This is my solution of project work of Web Inteligence course at Aalborg University.

Project is going to implement simple web search engine.

All the important implementation stuff can be found in lib directory. the-crawler.py is just a script that instantiates a crawler object, starts the crawling then builds the index and enables user to enter search queries.

So far you can find the following features implemented:

* Crawler logic that downloads webpages stored in queue
* HTML document parser that extracts all the URLs from HTML document
* HTML document parser that strips all HTML from document and stores just the pure text
* robots.txt parser that can parse the file and verify whether a link should be crawled or not
* Indexer logic that builds the inverted index
* Tokens are stemmed using NLTK Snowball stemmer, stop words and punctuation is removed.
* Index holds the information of token occurences in the set of documents and then number of occurences in every single document.
* Boolean Search Model based on stacking functions that return result lists
