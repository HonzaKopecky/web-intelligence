from html.parser import HTMLParser
import re

class Parser:

	#remember that we are accepting only full links 
	def getLinks(self, document):
		links = set()
		toRemove = set()
		links = FullLinksParser().getLinks(document)
		for link in links:
			if not self.validateURL(link):
				toRemove.add(link)
		for rem in toRemove:
			links.remove(rem);
		return links

	def strip_tags(self,html):
		s = MLStripper()
		scriptRegex = re.compile(r'<script.*?</script>(?s)', re.DOTALL)
		html = scriptRegex.sub('', html)
		s.feed(html)
		text = s.get_data()
		text = re.sub('[\n\t ]+', ' ', text)
		return text

	def getText(self, input):
		return self.strip_tags(input)

	def validateURL(self, url):
		regex = re.compile(
			r'^(?:http|ftp)s?://' # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
			r'localhost|' # localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
			r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
			r'(?::\d+)?' # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)
		return re.match(regex,url) is not None;

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.strict = False
		self.convert_charrefs= True
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)

	def get_data(self):
		return ''.join(self.fed)

class FullLinksParser:
	def getLinks(self, document): 
		links = set()
		aTagsRegex = re.compile("<a.*?>")
		aTags = aTagsRegex.findall(document)
		for aTag in aTags:
			url = re.search("https?://[^\"]*", aTag)
			if url is None:
				continue
			links.add(url.group(0))
		return links