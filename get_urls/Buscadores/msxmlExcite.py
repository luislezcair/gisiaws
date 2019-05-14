# -*- coding: utf-8 -*-

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from BeautifulSoup import BeautifulSoup


def generar_consulta_excite(consultas):
    urls = []
    for consulta in consultas:
        try:
            driver = webdriver.PhantomJS()
            driver.set_script_timeout(30)
            driver.maximize_window()
            consulta = consulta.replace(" ","+")

            # Esta URL da problemas con la conexión mediante el proxy de UGD
            # driver.get("http://msxml.excite.com/info.xcite/search/web?fcoid=417&fcop=topnav&fpid=27&q="+str(consulta))
            
            # Esta funciona. Las URLs se deben parsear de forma distinta como dice más abajo
            driver.get("https://search.excite.com/search/web?q="+str(consulta))

            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.searchResult")))
            except TimeoutException as e:
                print e
                next
            else:
                ids = driver.find_element_by_id('resultsMain')
                soup = BeautifulSoup(ids.get_attribute('innerHTML'))
                for url in soup.findAll('a',{"class":"resultTitle"}):
                    una_url = str(url['href'])
                    una_url_aux = una_url
                    una_url = una_url.split("%26du%3d")

                    # Esta línea es para la URL http://msxml.excite.com....
                    # aux = una_url[1].split("%26hash");

                    # Esta línea es para la URL https://search.excite.com....
                    aux = una_url[1].split("%26pct");

                    url = aux[0].replace("%253a",":").replace("%252f","/")

                    if 'https' not in url:
                        url = "http://" + str(url)

                    if "..." in url:
                        url = una_url_aux
                        driver.get(url)
                        url = driver.current_url
                    urls.append(url)

                driver.quit()
        except Exception as e:
            print str(e)
            print "Error consulta " + consulta
            pass
    return urls
