#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import commands
import json
from pattern.web import URL, plaintext, MIMETYPE_PDF,extension
import glob
import itertools
from webminer.controllers import *
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from webminer.models.config import *

'''
Clase que se encarga de descargar el contenido de cada url y guardarlo en un archivo.
'''

class WebScraperClass:

    #fileGenerator=None

    def __init__(self):
        self.fileGenerator=FileGenerator()


    def htmlToText(self,url):
        htmlContent = URL(url).download()
        #htmlContent = plaintext(s, keep={'h1':[], 'h2':[], 'strong':[], 'a':['href']})
        txtContent = plaintext(htmlContent, keep={'a':['href']})
        return htmlContent
    
    '''
    Inicio del scraper.
    @scrpaerLinks: conjunto de enlaces para descargar
    @progress: objeto para indicar el progreso del webminer.
    @directorio: ubicacion para el almacenamiento de archivos.
    @id_request del proyecto ejecutado.
    @searchKey: consulta de busqueda.
    '''
    def start(self,scraperLinks,progress,directorio,id_request,searchKey):
        unConfig = config()
        step=0
        progress.set_totalScraping(len(scraperLinks))
        progress.set_scrapingState('Ejecutando')

        # ordenar por el peso de los documentos
        self.rankear(scraperLinks,searchKey)

        scraperLinks = sorted(scraperLinks, key=lambda k: k['totalScore'])
        scraperLinks = self.unificarLista(scraperLinks)
        self.crearTop50(scraperLinks,directorio,unConfig)

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

        #limpieza json


        if not progress.get_stop():
            progress.set_scrapingState('Finalizado')

        #Fix this
        try:
            os.chdir(unConfig.repositoryPath + directorio)
            for file in glob.glob('*.json'):
                archivo = open(unConfig.repositoryPath+directorio+"/"+file, 'r')
                if not archivo.read():
                    os.remove(unConfig.repositoryPath+directorio+"/"+file)
                    self.eliminarArchivos(unConfig.repositoryPath+directorio,str(file).split('.json')[0])
                    logController = LogsController(directorio)
                    logController.Warning("Json Eliminado: " + str(file))
        except Exception as e:
            logController = LogsController(directorio)
            logController.Error("L87 Scraper")
            print str(e)
            pass

    '''
    Se crean los top 50 documentos en archivos .txt.
    '''
    def crearTop50(self,scraperLinks,directorio,unConfig):
        filename = unConfig.pathLog+directorio+"top50.txt"
        if not os.path.isfile(filename):
            archivo = open(filename,'wb')
        else:
            archivo = open(filename,'a')
        for doc in scraperLinks[:50]:
            archivo.write(doc['link']+"\n")
        archivo.write("\n")
        archivo.close()

    '''
    Al generarse un nuevo top 50, se eliminan los existentes.    
    '''
    def eliminarArchivos(self,directorio,nombre):
        os.chdir(directorio)
        for file in glob.glob(nombre+".*"):
            os.remove(directorio+"/"+file)

    '''
    Metodo Ranking reciproco. Destinado a unificar diferentes ranking en una sola lista.
    Explicado en Metodos/RankingReciproco.
    Si la query contiene la palabra tea, se agrega el metodo Weigth_Wa
    '''
    def rankear(self,scraperLinks,searchKey):

        if "tea" in searchKey:
            scraperLinks = sorted(scraperLinks, key=lambda k: k['weight_WA'], reverse=True)
            #print "WA"
            for indice,link in enumerate(scraperLinks):
                link['totalScore'] = 1/(indice+1)
        scraperLinks = sorted(scraperLinks, key=lambda k: k['weight_CRANK'], reverse=True)

        #print "weight_CRANK"
        for indice,link in enumerate(scraperLinks):
            link['totalScore'] += 1/(indice+1)
        scraperLinks = sorted(scraperLinks, key=lambda k: k['weight_VSM'], reverse=True)

        #print "weight_VSM"
        for indice,link in enumerate(scraperLinks):
            link['totalScore'] += 1/(indice+1)
        scraperLinks = sorted(scraperLinks, key=lambda k: k['weight_OKAPI'], reverse=True)

        #print "weight_OKAPI"
        for indice,link in enumerate(scraperLinks):
            link['totalScore'] += 1/(indice+1)

        for link in scraperLinks:
            link['totalScore'] = 1 / float(link['totalScore'])

    '''
    Metodo para unificar la lista. Evita duplicados y solo presenta uno por dominio.
    Luego, aquellas paginas con el mismo dominio son agrupados en colecciones internas.
    '''
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
                # print dominio
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

'''
Clase para generar los archivos.
'''
class FileGenerator:
    config = None
    repositoryPath = ""
    def __init__(self):
        self.config = config()
        self.repositoryPath = self.config.repositoryPath
        pass
    
    '''
    El archivo .txt con el contenido del documento esta acompañado de un json.
    Este json contiene la metadata de dicho documento. 
    Metadata: Url, Peso, Nombre del txt asociado, id_request, urls del mismo dominio (ordenados).
    '''
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

        # Creacion del json y verificacion de la existencia del html en .txt #
        self.write_file(minePackageLink,fileNameDocument,directorio)
        ruta = self.repositoryPath
        if not open(ruta + directorio + "/" + fileNameDocument,'r'):
            logController = LogsController(directorio)
            logController.Warning("No existe html: " + str(fileNameDocument))
        else:
            self.write_json(fileNameJson,document,directorio)
            if not open(ruta + directorio + "/" + fileNameJson, 'r').read():
                logController = LogsController(directorio)
                logController.Warning("Json Vacio: " + str(fileNameJson))



    '''
    Limpieza del directorio.
    Para una nueva lista, se recorre los 50 documentos.
    Si coincide la tupla (url,orden) no se elimina. Caso contrario se elimina y se crea un archivo nuevo
    '''
    def limpiarDirectorio(self, nombreArchivo ="*.json", directorio=""):
        try:
            unConfig = config()
            os.chdir(unConfig.repositoryPath + directorio)
            for file in glob.glob(nombreArchivo):
                archivo = open(unConfig.repositoryPath+directorio+"/"+file, 'r')
                if not archivo.read():
                    os.remove(unConfig.repositoryPath+directorio+"/"+file)
                    self.eliminarArchivos(unConfig.repositoryPath+directorio,str(file).split('.json')[0])
                    logController = LogsController(directorio)
                    logController.Warning("Json Eliminado: " + str(file))
        except Exception as e:
            logController = LogsController(directorio)
            print str(e)
            pass

    '''
    Escritura del json.    
    '''
    def write_json(self,fileName, structure , directorio):
        ruta = self.repositoryPath
        self.crearDirectorio(ruta,directorio)
        f = open(ruta+directorio+"/"+fileName, mode='w')
        orden = fileName[:2]
        os.chdir(ruta+directorio)
        for file in glob.glob(orden+"_*.json"):
            if(file != fileName):
                # print file
                fEliminar = open(ruta+directorio+"/"+file,'r')
                archivo = json.loads(fEliminar.read())
                try:
                    os.remove(ruta+directorio+"/"+archivo['document'][0]['filename'])
                except Exception as e:
                    print "Exception importante"
                    logController = LogsController(directorio)
                    logController.Error('L178 - Error Descarga: ' + fileName + ": " + str(e))
                    pass
                os.remove(ruta+directorio+"/"+file)
        if not structure:
            logController = LogsController(directorio)
            logController.Warning('L182 - Contenido Vacio')
        json.dump(structure, f, indent=2)
    
    '''
    Escritura del html en .txt    
    '''
    def write_file(self,minePackageLink,fileName , directorio):
        ruta = self.repositoryPath
        self.crearDirectorio(ruta,directorio)

        nombreFile,extensionFile = os.path.splitext(fileName)
        self.comprobarArchivosExtras(directorio,nombreFile,extensionFile,ruta)

        if ".pdf" in fileName:
            url = URL(minePackageLink['link']).download(user_agent='Mozilla/5.0')
            document = open(ruta+directorio+"/"+fileName,'w')
            document.write(url)
            document.close()
            return True
        else:
            try:
                contenido =  minePackageLink['methodData'].contenidoConEtiquetas
                if contenido == None:
                    contenido = self.descargarContenido(minePackageLink['link'])
                f = open(ruta+directorio+"/"+fileName, mode='wb')
                f.write(contenido)
                f.close()
                return True
            except Exception as e:
                print "Excepcion escribir archivo --> " + fileName + " - " + str(e)
                pass
                return False
    '''
    Metodo para limpiar archivos extras generados por error.
    '''
    def comprobarArchivosExtras(self,directorio,nombreFile,extensionFile,ruta):
        numeroFila = nombreFile[:2]
        if len(glob.glob(numeroFila + "*")) > 2:
            for unArchivo in glob.glob(numeroFila+"*"):
                unArchivoName,unArchivoExtension = os.path.splitext(unArchivo)
                if (unArchivoExtension != extensionFile or unArchivoName != nombreFile) and unArchivoExtension != ".json" :
                    os.remove(ruta + directorio + "/" + unArchivo)
                    logController = LogsController(directorio)
                    logController.Warning('Mas de 3 archivos: ' + numeroFila)
                    logController.Info("Archivo Eliminado " + unArchivo)

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
        return htmlContent
        

