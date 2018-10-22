class Document:
	def __init__(self, docID, url, text, outboundLinks):
		self.id = docID
		self.url = url
		self.rawText = text
		self.links = outboundLinks
		self.score = 0