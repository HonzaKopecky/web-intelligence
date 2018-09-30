class Document:
	def __init__(self, docID, text, outboundLinks):
		self.id = docID
		self.rawText = text
		self.links = outboundLinks