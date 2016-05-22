import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pattern.web import URL, plaintext

class UrlToplainTextConverter:
	
	def __init__(self):
		pass

	def plainTextConverter(self,url):
		page = URL(url).download(user_agent='Mozilla/5')
		return plaintext(page, keep={}) 

class PdfToplainTextConverter:

	def __init__(self):
		pass


#obj = UrlToplainTextConverter()
#text = obj.plainTextConverter('https://docs.python.org/2/genindex.html')
#print text