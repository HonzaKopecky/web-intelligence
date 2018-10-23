class Document:
    def __init__(self, doc_id, url, text, outbound_links):
        self.id = doc_id
        self.url = url
        self.rawText = text
        self.links = outbound_links
        self.score = 0
