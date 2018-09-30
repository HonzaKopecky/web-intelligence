from urllib import request
from urllib import error

class Downloader:
	def downloadURL(self, url):
		file = self.downloadURLasFile(url)
		if file is None or file is False:
			return None
		return file.read()

	def downloadURLasFile(self, url):
		try:
			result = request.urlopen(url)
		except error.HTTPError as er:
			#If we get 404 error file was not found
			if er.code == 404:
				return None
			#In case we get an error other than "NOT FOUND" file cannot be downloaded
			return False
		except error.URLError:
			#In case  URL was not recognized (DNS errors mostly) file cannot be downloaded
			return False

		return result
