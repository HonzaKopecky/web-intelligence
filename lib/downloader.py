from urllib import request
from urllib import error


class Downloader:
	def download_url(self, url, content_type = None):
		file = self.download_as_file(url)
		if file is None or file is False:
			return None
		if content_type is not None:
			ct = ''.join(file.info()['Content-type'].split())
			ct = ct.lower()
			if ct != content_type:
				return None
		return file.read()

	@staticmethod
	def download_as_file(url):
		req = request.Request(url)
		try:
			return request.urlopen(req)
		except error.HTTPError as er:
			# If we get 404 error file was not found
			if er.code == 404:
				return None
			# In case we get an error other than "NOT FOUND" file cannot be downloaded
			return False
		except:
			# In case  URL was not recognized (DNS errors mostly) file cannot be downloaded
			# In case of SSL errors (invalid certificate)
			return False
