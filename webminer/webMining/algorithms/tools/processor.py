from pattern.vector import stem, PORTER, LEMMA, count, words
from pattern.en import parse, Sentence
#from plainTextConverter import UrlToplainTextConverter

class TextProcessor:
	def __init__(self):
		pass

	def stemmer(self,word):
		#stemmer=None, stemmer=LEMMA, stemmer=PORTER
		print stem(word,stemmer=PORTER)
		#print stem(word, stemmer=LEMMA)
		
	def tokenizer(self,url):
		#text = 'The black cat was spying on the white cat.'
		#stemmer=None, stemmer=LEMMA, stemmer=PORTER
		#print count(words(pageContent), stemmer=PORTER)
		#print count(words(pageContent), stemmer=LEMMA)


		#url_content = UrlToplainTextConverter()
		#page_content = url_content.plainTextConverter(url)
           page_content = url
           s = Sentence(parse(page_content))
           tokenized_file = count(words(s), stemmer=PORTER)
           print 
           print tokenized_file
           print
           #document = sorted(tokenized_file.items(),key = lambda x:x[0])
           #total_words=len(document)
           #document.append((total_words,url))
           #print document
           #print stem('computing', stemmer=LEMMA)
		#format output: [(u'word',tf),...,(total_words,url)]
           #print document
		
		
obj = TextProcessor()
#obj.tokenizer('india tea production statistics')
obj.tokenizer('mathematical ceiling supports signed zeros  Python Python Python expression big big big bigdf')

