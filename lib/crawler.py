import queue
import pickle
from .downloader import Downloader
from .document import Document
from .parser import Parser
from .robotParser import RobotParser

class Crawler:
	def __init__(self, limit):
		self.limit = limit
		self.documents = list()
		self.checked = set()
		self.urlQueue = queue.Queue()
		self.robotsCache = dict()

	def addSeed(self, url):
		self.urlQueue.put(url)
		self.checked.add(url)

	def crawl(self):
		while len(self.documents) < self.limit and not self.urlQueue.empty():
			link = self.urlQueue.get()
			print(link)
			if not RobotParser(self.robotsCache).canCrawl(link):
				print("\t skip")
				continue
			self.processURL(link)
			pass

	def processURL(self, url):
		rawContent = Downloader().downloadURL(url)
		try:
			decoded = rawContent.decode('utf-8')
		except:
			#sometimes decoding to UTF-8 fails, so we do not crawl the page
			return
		p = Parser()
		links = p.getLinks(decoded)
		newDocID = len(self.documents)
		self.documents.append(Document(newDocID, p.getText(decoded), links));
		self.addLinksToQueue(links)

	def addLinksToQueue(self, links):
		for link in links:
			if link not in self.checked:
				self.urlQueue.put(link)
				self.checked.add(link)

	def saveDocuments(self, path):
		f = open(path, "wb")
		pickle.dump(self.documents, f)
		f.close()

	@staticmethod
	def loadDocuments(path):
		f = open(path, "rb")
		docs = pickle.load(f)
		return docs



