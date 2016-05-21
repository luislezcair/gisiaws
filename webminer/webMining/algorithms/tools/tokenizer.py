import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pattern.en import tag
from pattern.web import URL, plaintext

class Tokenizer:
	def __init__(self):
		pass

	def tokenizer(self,url):
     
		#page = URL(url).download(user_agent='Mozilla/5')
           page = URL(url).download()
           text = plaintext(page, keep={})
           tokens = tag(text)
		#print tokens
           print len(tokens),' words'
           document=[]
           while tokens:
			document.append(tokens.pop(0)[0])
		#print document

obj = Tokenizer()
#obj.tokenizer('http://www.pureceylontea.com/index.php/features/fine-ceylon-tea/manufacturing')
#obj.tokenizer('http://www.clips.ua.ac.be/pages/pattern-en')

