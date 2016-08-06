#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import commands
import json
from pattern.web import URL, plaintext, MIMETYPE_PDF,extension
import glob
import itertools

try:
    from settings_local import *
except ImportError:
    # Establece el directorio por defecto del repositorio si no encuentra el
    # archivo de configuración.
    # El archivo settings.py debe tener esta misma línea:
    REPOSITORY_PATH = '/var/www/html/gisiaws/webminer/webScraper/storage/'


class WebScraperClass:

    #fileGenerator=None

    def __init__(self):
        self.fileGenerator=FileGenerator()

    def htmlToText(self,url):
        htmlContent = URL(url).download()
        #htmlContent = plaintext(s, keep={'h1':[], 'h2':[], 'strong':[], 'a':['href']})
        txtContent = plaintext(htmlContent, keep={'a':['href']})
        return htmlContent

    def pdfToText(self,link):
        url = URL(link)
        document = open ('temp.pdf','w')
        document.close()
        download = url.download()
        document = open('temp.pdf','a')
        document.write(download)
        document.close()
        #content=os.system('pdf2txt.py temp.pdf')
        txtContent=commands.getoutput('pdf2txt.py temp.pdf')
        return txtContent

    def start(self,scraperLinks,progress,directorio,id_request,searchKey):
        step=0
        progress.set_totalScraping(len(scraperLinks))
        progress.set_scrapingState('Ejecutando')

        # ordenar por el peso de los documentos
        self.rankear(scraperLinks,searchKey)
        scraperLinks = sorted(scraperLinks, key=lambda k: k['totalScore'])
        scraperLinks = self.unificarLista(scraperLinks)


        progress.totalNodes = len(scraperLinks)
        for link in scraperLinks:
            if not progress.get_stop():
                step+=1
                progress.set_scrapingProgress(step)
                url=URL(link['link'])
                fileNameJson = str(step).zfill(2)+"_"+url.domain+'.json'
                fileNameDocument = str(step).zfill(2)+"_"+url.domain
                if extension(url.page) == ".pdf":
                    fileNameDocument += ".pdf"
                else:
                    fileNameDocument += ".html"
                try:
                    self.fileGenerator.json(link,fileNameJson,fileNameDocument,link,id_request,directorio)
                except Exception,e:
                    print str(e)
                    pass
            else:
                progress.set_scrapingState('Detenido')
                print 'Detenido'
                break
        if not progress.get_stop():
            progress.set_scrapingState('Finalizado')

    def rankear(self,scraperLinks,searchKey):
        if "tea" in searchKey:
            scraperLinks = sorted(scraperLinks, key=lambda k: k['weight_WA'], reverse=True)
            print "WA"
            for indice,link in enumerate(scraperLinks):
                link['totalScore'] = indice
        scraperLinks = sorted(scraperLinks, key=lambda k: k['weight_CRANK'], reverse=True)
        print
        print "weight_CRANK"
        for indice,link in enumerate(scraperLinks):
            link['totalScore'] += indice
        scraperLinks = sorted(scraperLinks, key=lambda k: k['weight_VSM'], reverse=True)
        print
        print "weight_VSM"
        for indice,link in enumerate(scraperLinks):
            link['totalScore'] += indice
        scraperLinks = sorted(scraperLinks, key=lambda k: k['weight_OKAPI'], reverse=True)
        print
        print "weight_OKAPI"
        for indice,link in enumerate(scraperLinks):
            link['totalScore'] += indice

    def unificarLista(self,scraperLinks):
        listaDominios = []
        listaUrls = []
        contador = 0
        for unLink in scraperLinks:
            if contador == 50:
                return listaUrls
            unaUrl = URL(unLink['link'])
            dominio = unaUrl.domain
            if dominio not in listaDominios:
                print dominio
                unLink['urlsDominio'] = []
                listaDominios.append(dominio)
                listaUrls.append(unLink)
                contador +=1
            else:
                for unEnlace in listaUrls:
                    otraUrl = URL(unEnlace['link'])
                    otroDominio = otraUrl.domain
                    if(dominio == otroDominio):
                        unaUrlDominio = {}
                        unaUrlDominio['url'] = unLink['link']
                        unEnlace['urlsDominio'].append(unaUrlDominio['url'])
        return listaUrls

    def contarEnlaces(self,listaUrls):
        contador = 0
        for unaUrl in listaUrls:
            for otraUrl in unaUrl['urlsDominio']:
                contador += 1
            contador+=1
        return contador
class FileGenerator:

    def __init__(self):
        pass

    def json(self,minePackageLink,fileNameJson,fileNameDocument,link,id_request,directorio):
        document={}
        webContent={}
        contentList=[]
        webContent['url'] = link['link']
        webContent['weight'] = link['totalScore']
        webContent["filename"]=fileNameDocument
        webContent["id_request"] = id_request
        webContent['urlsDominio'] = link['urlsDominio']
        contentList.append(webContent)
        document["document"]=contentList

        self.write_file(minePackageLink,fileNameDocument,directorio,link)
        self.write_json(fileNameJson,document,directorio)


    def write_json(self,fileName, structure , directorio):
        ruta = REPOSITORY_PATH
        self.crearDirectorio(ruta,directorio)
        f = open(ruta+directorio+"/"+fileName, mode='w')
        orden = fileName[:2]

        os.chdir(ruta+directorio)
        for file in glob.glob(orden+"_*.json"):
            if(file != fileName):
                print file
                fEliminar = open(ruta+directorio+"/"+file,'r')
                archivo = json.loads(fEliminar.read())
                try:
                    os.remove(ruta+directorio+"/"+archivo['document'][0]['filename'])
                except:
                    pass
                os.remove(ruta+directorio+"/"+file)
        json.dump(structure, f, indent=2)

    def write_file(self,minePackageLink,fileName , directorio,link):
        ruta = REPOSITORY_PATH
        self.crearDirectorio(ruta,directorio)

        if ".pdf" in fileName:
            url = URL(minePackageLink['link']).download(user_agent='Mozilla/5.0')
            document = open(ruta+directorio+"/"+fileName,'w')
            document.write(url)
            document.close()
        else:
            try:
                contenido =  minePackageLink['methodData'].contenidoConEtiquetas
                try:
                    if contenido == None:
                        contenido = self.descargarContenido(minePackageLink['link'])
                except:
                    pass
                f = open(ruta+directorio+"/"+fileName, mode='w')
                json.dump(contenido, f, indent=2)
                f.close()
            except:
                print "Excepcion escribir archivo --> " + link
                pass

    def html(self,content):
        pass

    def xhtml(self,content):
        pass

    def xml(self,content):
        pass

    def crearDirectorio(self,ruta,nombre_directorio):
        newpath = ruta + nombre_directorio
        if not os.path.exists(newpath):
            os.makedirs(newpath)

    def descargarContenido(self,link):
        htmlContent = URL(link).download()
        htmlContent = plaintext(htmlContent, keep={'title':[],'h1':[], 'h2':[], 'strong':[]})
        return htmlContent.replace("\n\n","<br>").replace("\n"," ")
#obj=WebScraperClass()
#obj.start(['http://www.clips.ua.ac.be/sites/default/files/ctrs-002_0.pdf'])
#obj.start(['http://www.teaboard.gov.in/pdf/notice/Plant_Protection_Code_Ver_5_0_January_2016.pdf'])
