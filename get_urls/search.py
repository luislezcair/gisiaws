# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import json
from model.Proyecto import *


def obtener_urls(data):

    proyecto = Proyecto() #creamos un objeto Proyecto.
    proyecto.setId(int(data["id_proyecto"]))
    proyecto.setNombreDirectorio(data["nombre_directorio"])

    for clave in data["claves"]:
        proyecto.agregarClaves(clave["clave"])

    proyecto.generarUrl(proyecto.claves)
    # proyecto.generarMensajeJson()

    data_json = proyecto.generarMensajeJson()

    # data_response = json.dumps(data_json, indent=4, sort_keys=False)  

    # #crear .txt
    # archi=open('json.txt','w')
    # archi.write(json.dumps(data_json, indent=4, sort_keys=False))
    # archi.close()

    # return data_response
    return data_json
