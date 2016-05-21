from pattern.web import URL
import re

class Filter:

    def __init__(self):
        self.badLinks='youtube|linkedin|wikipedia|amazon|books.google|facebook|twitter|instagram|plus.google|yahoo|ebay|ebayinc|flickr|t.co|.google.|youtu.be|microsoft|microsoftstore'

    def detect(self,link):
        url=URL(link)
        #print url.domain
        if re.search(self.badLinks,url.domain)!=None:
            bad=True
        else:
            bad=False
        return bad

'''
link1='es.wikipedia.org'
link2='en.wikipedia.org/asdasd/asdasda/dsad.html'
link3='sri.lacienciadelte_tea.com'
link4='www.youtube.com'
link5='https://books.google.com.ar/books?id=ZQMBSSOVUyAC&printsec=frontcover&hl=es&source=gbs_ge_summary_r&cad=0#v=onepage&q&f=false'
obj=Filter()
print obj.detect('http://twitter.com/self')
'''