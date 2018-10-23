class Document:
    def __init__(self, doc_id, url, text, outbound_links):
        self.id = doc_id
        self.url = url
        self.raw_text = text
        self.links = outbound_links
        self.score = 0
        self.page_rank = 0
