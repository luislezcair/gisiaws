# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import os
import sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pattern.web import Bing, asynchronous, plaintext, URL  , SEARCH , time
import bs4 as bs
import urllib2

def generar_consulta_bing(q):    
    reload(sys)
    sys.setdefaultencoding('utf8')

    engine_bing = Bing(license="TNMHm68dvf440pSPdnU+2LqxeQi7J2xszPZLBiPYsmI", language="en")
    bing = []
    for consulta in q:
        request = asynchronous(engine_bing.search, consulta, start=1, count=10, type=SEARCH, timeout=10)

        while not request.done:
            time.sleep(0.01)

        # An error occured in engine.search(), raise it.
        if request.error:
            raise request.error

        # Retrieve the list of search results.
        for result in request.value:
            bing.append(result.url)

    return bing


# Metodo que utiliza la libreria beautifulsoup para obtener las urls de la busqueda.
# Se ejecuta cuando el primer metodo falla
def recuperar_urls_beautifulsoup(q):
    bing = []
    for consulta in q:
        consulta = consulta.replace(" ", "+")

        sauce = urllib2.urlopen("https://www.bing.com/search?q=" + consulta).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        divs = soup.findAll("li", {"class": "b_algo"})
        for unDivs in divs:
            bing.append(unDivs.find('a').get('href'))
    return bing
