# Web crawler for Web Intelligence course at AAU

This is my solution of project work of Web Inteligence course at Aalborg University.

Project is going to implement simple web crawler.

All the important implementation stuff can be found in lib directory. the-crawler.py is just a script that instantiates a crawler object and starts the crawling.

So far you can find the following features implemented:

* Crawler logic that downloads webpages stored in queue
* HTML document parser that extracts all the URLs from HTML document
* HTML document parser that strips all HTML from document and stores just the pure text
* robots.txt parser that can parse the file and verify whether a link should be crawled or not
