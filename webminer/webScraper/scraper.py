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
        return txtContent

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
        scraperLinks = sorted(scraperLinks, key=lambda k: k['weight'], reverse=True)
        for link in scraperLinks:
            if not progress.get_stop():
                step+=1
                progress.set_scrapingProgress(step)
                url=URL(link['link'])
                # fileName='file_'+str(step)+'.json'
                fileName = str(id_request)+"-"+str(step)+"@"+url.domain+'.json'
                print '->'+fileName
                if url.mimetype in MIMETYPE_PDF:
                    self.fileGenerator.json(fileName,self.pdfToText(link['link']),link['link'],link['weight'],directorio)
                else:
                    self.fileGenerator.json(fileName,self.htmlToText(link['link']),link['link'],link['weight'],directorio)
            else:
                progress.set_scrapingState('Detenido')
                print 'Detenido'
                break
        if not progress.get_stop():
            progress.set_scrapingState('Finalizado')


class FileGenerator:

    def __init__(self):
        pass

    def json(self,fileName,content,link,weight,directorio):
        document={}
        webContent={}
        contentList=[]
        webContent['url'] = link
        webContent['weight'] = weight
        webContent["content"]=content
        contentList.append(webContent)
        document["document"]=contentList
        self.write_json(fileName,document,directorio)

    def write_json(self,fileName, structure , directorio):
        ruta = REPOSITORY_PATH
        self.crearDirectorio(ruta,directorio)
        f = open(ruta+directorio+"/"+fileName, mode='w')
        json.dump(structure, f, indent=2)
        f.close()

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

#obj=WebScraperClass()
#obj.start(['http://www.clips.ua.ac.be/sites/default/files/ctrs-002_0.pdf'])
#obj.start(['http://www.teaboard.gov.in/pdf/notice/Plant_Protection_Code_Ver_5_0_January_2016.pdf'])
