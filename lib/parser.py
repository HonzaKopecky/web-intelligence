from html.parser import HTMLParser
import re
import string


class Parser:
    # remember that we are accepting only full links
    def get_links(self, document):
        to_remove = set()
        links = set(FullLinksParser().get_links(document))
        for link in links:
            if not self.validate_url(link):
                to_remove.add(link)
        for rem in to_remove:
            links.remove(rem);
        return links

    @staticmethod
    def strip_tags(html):
        s = MLStripper()
        script_regex = re.compile(r'<script.*?</script>(?s)', re.DOTALL)
        style_regex = re.compile(r'<style.*?</style>(?s)', re.DOTALL)
        html = script_regex.sub('', html)
        html = style_regex.sub('',html)
        s.feed(html)
        text = s.get_data()
        text = ' '.join(text.split())
        table = str.maketrans("","",string.punctuation)
        text = text.translate(table)
        return text

    def get_text(self, input):
        return self.strip_tags(input)

    def validate_url(self, url):
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
    def error(self, message):
        pass

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ' '.join(self.fed)


class FullLinksParser:
    def get_links(self, document):
        links = set()
        a_tags_regex = re.compile("<a.*?>")
        aTags = a_tags_regex.findall(document)
        for aTag in aTags:
            url = re.search("https?://[^\"]*", aTag)
            if url is None:
                continue
            links.add(url.group(0))
        return links
