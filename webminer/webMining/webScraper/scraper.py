#!/usr/bin/python
# -*- coding: utf-8 -*-
#import os
import commands
import json
from pattern.web import URL, plaintext, MIMETYPE_PDF



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

    def start(self,scraperLinks,progress):
        step=0
        progress.set_totalScraping(len(scraperLinks))
        progress.set_scrapingState('Ejecutando')
        for link in scraperLinks:
            if not progress.get_stop():
                step+=1
                progress.set_scrapingProgress(step)
                url=URL(link)
                fileName='file_'+str(step)+'.json'
                print '->'+fileName
                if url.mimetype in MIMETYPE_PDF:
                    self.fileGenerator.json(fileName,self.pdfToText(link))
                else:
                    self.fileGenerator.json(fileName,self.htmlToText(link))
            else:
                progress.set_scrapingState('Detenido')
                print 'Detenido'
                break
        if not progress.get_stop():
            progress.set_scrapingState('Finalizado')


class FileGenerator:
    
    def __init__(self):
        pass

    def json(self,fileName,content):
        document={}
        webContent={}
        contentList=[]
        webContent["content"]=content
        contentList.append(webContent)
        document["document"]=contentList
        self.write_json(fileName,document)
    
    def write_json(self,fileName, structure):
        f = open("/home/matt/clusterProject/webMining/webScraper/storage/"+fileName, mode='w')
        json.dump(structure, f, indent=2)
        f.close()
    
    def html(self,content):
        pass

    def xhtml(self,content):
        pass

    def xml(self,content):
        pass

#obj=WebScraperClass()
#obj.start(['http://www.clips.ua.ac.be/sites/default/files/ctrs-002_0.pdf'])
#obj.start(['http://www.teaboard.gov.in/pdf/notice/Plant_Protection_Code_Ver_5_0_January_2016.pdf'])   