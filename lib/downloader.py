from urllib import request
from urllib import error

class Downloader:
	def downloadURL(self, url, contentType = None):
		file = self.downloadURLasFile(url)
		if file is None or file is False:
			return None
		if contentType is not None:
			if file.info()['Content-type'] != contentType:
				return None
		return file.read()

	def downloadURLasFile(self, url):
		req = request.Request(url)

		try:
			return request.urlopen(req)
		except error.HTTPError as er:
			#If we get 404 error file was not found
			if er.code == 404:
				return None
			#In case we get an error other than "NOT FOUND" file cannot be downloaded
			return False
		except:
			#In case  URL was not recognized (DNS errors mostly) file cannot be downloaded
			#In case of SSL errors (invalid certificate)
			return False

		return result
