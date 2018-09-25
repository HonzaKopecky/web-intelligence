import queue
from .downloader import Downloader
from .document import Document
from .parser import Parser
from .robotParser import RobotParser

class Crawler:
	def __init__(self, limit):
		self.limit = limit
		self.documents = set()
		self.checked = set()
		self.urlQueue = queue.Queue()
		self.robotsCache = dict()

	def addSeed(self, url):
		self.urlQueue.put(url)

	def crawl(self):
		while len(self.documents) < self.limit and not self.urlQueue.empty():
			link = self.urlQueue.get()
			self.checked.add(link)
			print(link)
			if not RobotParser(self.robotsCache).canCrawl(link):
				print("\t Cannot crawl - skipping.")
				continue
			self.processURL(link)
			pass

	def processURL(self, url):
		rawContent = Downloader().downloadURL(url)
		try:
			decoded = rawContent.decode('utf-8')
		except AttributeError:
			print("\t Cannot convert to utf-8.");
			return
		p = Parser()
		links = p.getLinks(decoded)
		self.documents.add(Document(p.getText(decoded),links))
		self.addLinksToQueue(links)

	def addLinksToQueue(self, links):
		for link in links:
			if link not in self.checked:
				self.urlQueue.put(link)
