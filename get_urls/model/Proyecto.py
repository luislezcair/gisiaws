# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from get_urls.Buscadores.google import *
from get_urls.Buscadores.bing import *
from get_urls.Buscadores.msxmlExcite import *
from get_urls.Buscadores.intelligo import *

class Proyecto:
    def __init__(self):
        self.id = ""
        self.nombre_directorio = ""
        self.claves = []
        self.url_google = []
        self.url_bing = []
        self.url_excite = []
        self.url_intelligo = []

    def setId(self, un_id):
        self.id = un_id

    def setNombreDirectorio(self, nombre_directorio):
        self.nombre_directorio = nombre_directorio

    def agregarClaves(self, clave):
        self.claves.append(clave)

    def generarUrl(self, consulta):
        # try:
        #     self.url_google.append(generar_consulta_google(consulta))
        # except:
        #     print "Excepcion: google"
        #     pass
        # try:
        #     self.url_bing.append(generar_consulta_bing(consulta))
        # except:
        #     print "Excepcion: bing"
        #     pass
        # try:
        #     self.url_excite.append(generar_consulta_excite(consulta))
        # except:
        #     print "Excepcion: excite"
        #     pass
        # try:
        #     self.url_intelligo.append(generar_consulta_intelligo(consulta))
        # except:
        #     print "Excepcion: intelligo"
        #     pass
        pass
    def crear_buscador_json(self, nombre_buscador, urls):
        buscador = {}
        buscador['buscador'] = nombre_buscador
        buscador['urls'] = []
        for links in urls:
            for un_link in links:
                url = {}
                url['url'] = un_link
                buscador['urls'].append(url)
        return buscador

    def generarMensajeJson(self):
        data_json = {}
        data_json['id_proyecto'] = self.id
        data_json['buscadores'] = []
        data_json['buscadores'].append(self.crear_buscador_json("Google", self.url_google))
        data_json['buscadores'].append(self.crear_buscador_json("Bing", self.url_bing))
        data_json['buscadores'].append(self.crear_buscador_json("Excite", self.url_excite))
        data_json['buscadores'].append(self.crear_buscador_json("Intelligo", self.url_intelligo))
        return data_json
