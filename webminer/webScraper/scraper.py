#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import commands
import json
from pattern.web import URL, plaintext, MIMETYPE_PDF

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

    def start(self,scraperLinks,progress,directorio,id_request):
        step=0
        progress.set_totalScraping(len(scraperLinks))
        progress.set_scrapingState('Ejecutando')

        # ordenar por el peso de los documentos
        scraperLinks = sorted(scraperLinks, key=lambda k: k['totalScore'], reverse=True)
        for link in scraperLinks[:50]:
            if not progress.get_stop():
                step+=1
                progress.set_scrapingProgress(step)
                url=URL(link['link'])
                fileNameJson = str(step).zfill(2)+"_"+url.domain+'.json'
                fileNameDocument = str(step).zfill(2)+"_"+url.domain

                if url.mimetype in MIMETYPE_PDF:
                    fileNameDocument += ".pdf"
                else:
                    fileNameDocument += ".html"
                self.fileGenerator.json(fileNameJson,fileNameDocument,link['link'],link['totalScore'],id_request,directorio)
            else:
                progress.set_scrapingState('Detenido')
                print 'Detenido'
                break
        if not progress.get_stop():
            progress.set_scrapingState('Finalizado')


class FileGenerator:

    def __init__(self):
        pass

    def json(self,fileNameJson,fileNameDocument,link,weight,id_request,directorio):
        document={}
        webContent={}
        contentList=[]
        webContent['url'] = link
        webContent['weight'] = weight
        webContent["filename"]=fileNameDocument
        webContent["id_request"] = id_request
        contentList.append(webContent)
        document["document"]=contentList
        self.write_json(fileNameJson,document,directorio)
        self.write_file(fileNameDocument,directorio,link)

    def write_json(self,fileName, structure , directorio):
        ruta = REPOSITORY_PATH
        self.crearDirectorio(ruta,directorio)
        f = open(ruta+directorio+"/"+fileName, mode='w')
        json.dump(structure, f, indent=2)

    def write_file(self,fileName , directorio,link):
        ruta = REPOSITORY_PATH
        self.crearDirectorio(ruta,directorio)
        if "pdf" in fileName:
            url = URL(link).download()
            document = open (ruta+directorio+"/"+fileName,'w')
            document.write(url)
            document.close()
        else:
            try:
                contenido = self.descargarContenido(link)
                f = open(ruta+directorio+"/"+fileName, mode='w')
                json.dump(contenido, f, indent=2)
                f.close()
            except:
                print "Excepcion al descargar archivo --> " + link
                pass;

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
