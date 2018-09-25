from urllib import request
from urllib import error

class Downloader:
	def downloadURL(self, url):
		file = self.downloadURLasFile(url)
		if file is None:
			return None
		return file.read()

	def downloadURLasFile(self, url):
		try:
			result = request.urlopen(url)
		except error.HTTPError as er:
			if er.code != 404:
				raise FileNotFoundError("Something happened during robots.txt fetching. Error code: " + str(er.code));
			return None
		except error.URLError:
			raise FileNotFoundError("Robots file URL not recognized.");

		return result
