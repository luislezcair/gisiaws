#!/usr/bin/env python
# -*- coding:utf-8 -*-
import thread
import time
import tkMessageBox
from Tkinter import *
import Tkinter
import ttk

from webMining.algorithms.retrievalAlgorithms import *
from webMining.webMiner import *


class GUI:
    def __init__(self,ventana):
        self.query = StringVar()#query='Knowledge of Good Agricultural Practices'
        self.webMiner=None
        self.enfoquePonderado = WeightedApproach('WEIGHTED_APPROACH')
        self.cRank= CRank('C-RANK')
        self.supportVectorMachine = SupportVectorMachine('SUPPORT_VECTOR_MACHINE') 
        self.modeloEspacioVectorial = VectorSpaceModel('VECTORIAL_SPACE_MODEL')
        self.latentSemanticAnalysis = LatentSemanticAnalysis('LATENT_SEMANTIC_ANALYSIS')

        self.algoritmo=None
        self.progress=None
        self.linksGoogle=IntVar()
        self.linksBing=IntVar()
        self.cloudSize=IntVar()
        self.enlaces = range(11)
        self.cloud = range(11)
        self.colorFondoConsola="#000000"
        self.colorLetraConsola="#FFFFFF"
        self.progreso=StringVar()
        self.accion=StringVar()
        self.progresoCrawler=StringVar()
        self.accionCrawler=StringVar()
        self.progresoIR=StringVar()
        self.accionIR=StringVar()
        self.progresoScraping=StringVar()
        self.accionScraping=StringVar()
        self.totalCrawling=StringVar()
        self.totalScraping=StringVar()
        self.totalIR=StringVar()
        self.de=StringVar()
        self.estadoCrawling=StringVar()
        self.estadoScraping=StringVar()
        self.estadoIR=StringVar()


        ventana.title("Web miner   v1.0")
        ventana.geometry("950x550")
        self.lblConsulta = Label(ventana,text="Consulta: ").place(x=10,y=10)
        self.txtBoxConsulta = Entry(ventana,width =100,textvariable=self.query,bg="#FFF").place(x=80,y=10)
        self.query.set('Knowledge of Good Agricultural Practices')
        self.boton = Button(ventana, text="Ejecutar",command=self.comenzarProceso)
        self.boton.place(x=80,y=35)

        self.botonDetener = Button(ventana, text="Detener",command=self.detenerProceso)
        self.botonDetener.place(x=80,y=65)
        
        self.botonEstado = Button(ventana, text="Estado",command=self.verEstado)
        self.botonEstado.place(x=80,y=500)

        self.botonCerrar = Button(ventana, text="Cerrar programa",command=self.cerrarPrograma)
        self.botonCerrar.place(x=800,y=500)        

        self.lblEnlacesGoogle = Label(ventana,text="Links Google:").place(x=210,y=40)
        self.sBoxEnlacesGoogle = Spinbox(ventana,width=3,value=self.enlaces,textvariable=self.linksGoogle).place(x=293,y=40)
        self.lblEnlacesBing = Label(ventana,text="Links Bing:").place(x=360,y=40)
        self.sBoxEnlacesBing = Spinbox(ventana,width=3,value=self.enlaces,textvariable=self.linksBing).place(x=430,y=40)

        self.lblCloudSize = Label(ventana,text="cantidad de enlaces:").place(x=500,y=40)
        self.sBoxCloudSize = Spinbox(ventana,width=3,value=self.cloud,textvariable=self.cloudSize).place(x=630,y=40)

        self.lblTitulo = Label(ventana,text="Algoritmos RI:").place(x=700,y=100)
        self.radioBtnEnfoquePonderado = Radiobutton(ventana,text="Enfoque poderado",value=1,command=self.asignarEnfoquePonderado)
        self.radioBtnEnfoquePonderado.place(x=700,y=140)
        self.radioBtnCrank =  Radiobutton(ventana,text="C-Rank",value=2,command=self.asignarCrank)
        self.radioBtnCrank.place(x=700,y=160)
        self.radioBtnSvm =  Radiobutton(ventana,text="Support Vector Machine",value=3,command=self.asignarSupportVectorMachine)
        self.radioBtnSvm.place(x=700,y=180)
        self.radioBtnVectorial = Radiobutton(ventana,text="Vectorial",value=4,command=self.asignarVectorial)
        self.radioBtnVectorial.place(x=700,y=200)
        self.radioBtnSemantica = Radiobutton(ventana,text="Latent semantic analysis",value=6,command=self.asignarSemanticAnalysis)
        self.radioBtnSemantica.place(x=700,y=220)

        self.cajaTexto = Text(ventana, width = 75, height =10,bg=self.colorFondoConsola,fg=self.colorLetraConsola)
        self.cajaTexto.place(x=80,y=100)

        self.porcentaje=Label(ventana,text="",textvariable=self.progreso).place(x=147,y=280)
        self.proceso=Label(ventana,text="",textvariable=self.accion).place(x=80,y=280)
        self.progressBar=ttk.Progressbar(ventana,orient='horizontal',mode='determinate',length=530)
        self.progressBar.pack(expand=False, fill=Tkinter.BOTH, side=Tkinter.BOTTOM)
        self.progressBar.place(x="80",y="300")
        self.l1=Label(ventana,text="|").place(x=79,y=320)
        self.l2=Label(ventana,text="0%").place(x=79,y=340)
        self.l3=Label(ventana,text="|").place(x=340,y=320)
        self.l4=Label(ventana,text="50%").place(x=333,y=340)
        self.l5=Label(ventana,text="|").place(x=604,y=320)
        self.l6=Label(ventana,text="100%").place(x=591,y=340)

        self.crawler=Label(ventana,text="- Exploración de enlaces:",textvariable=self.accionCrawler).place(x=80,y=385)
        self.porcentajeCrawler=Label(ventana,text="0",textvariable=self.progresoCrawler).place(x=300,y=385)
        self.l7=Label(ventana,text="de",textvariable=self.de).place(x=400,y=385)
        self.l10=Label(ventana,text="100",textvariable=self.totalCrawling).place(x=450,y=385)
        self.l13=Label(ventana,text="",textvariable=self.estadoCrawling).place(x=500,y=385)

        self.informationRetrieval=Label(ventana,text="- Ranking de documentos:",textvariable=self.accionIR).place(x=80,y=420)
        self.porcentajeIR=Label(ventana,text="0",textvariable=self.progresoIR).place(x=300,y=420)
        self.l8=Label(ventana,text="de",textvariable=self.de).place(x=400,y=420)
        self.l11=Label(ventana,text="100",textvariable=self.totalIR).place(x=450,y=420)
        self.l14=Label(ventana,text="",textvariable=self.estadoIR).place(x=500,y=420)

        self.scraping=Label(ventana,text="- Extracción de contenido:",textvariable=self.accionScraping).place(x=80,y=455)
        self.porcentajeScraping=Label(ventana,text="0",textvariable=self.progresoScraping).place(x=300,y=455)
        self.l9=Label(ventana,text="de",textvariable=self.de).place(x=400,y=455)
        self.l12=Label(ventana,text="100",textvariable=self.totalScraping).place(x=450,y=455)
        self.l15=Label(ventana,text="",textvariable=self.estadoScraping).place(x=500,y=455)


    def detenerProceso(self):
        self.webMiner.stopWebMiner()
    
    def verEstado(self):
        self.webMiner.getState()
    
    def cerrarPrograma(self):
        thread.exit_thread()

    def comenzarProceso(self):
        if self.algoritmo!=None:
            self.cajaTexto.config(state=NORMAL)
            self.cajaTexto.delete(1.0,END) 
            self.cajaTexto.insert(INSERT,"RECUPERACION DE INFORMACION WEB")
            self.cajaTexto.insert(INSERT,"\n--------------------------------------------------------------------------")
            self.cajaTexto.insert(INSERT,"\nConsulta: "+self.query.get())
            self.cajaTexto.insert(INSERT,"\nAlgoritmo: " +self.algoritmo.getName())
            self.cajaTexto.insert(INSERT,"\nLinks Google: "+str(self.linksGoogle.get()))
            self.cajaTexto.insert(INSERT,"\nLinks Bing: "+str(self.linksBing.get()))
            self.cajaTexto.insert(INSERT,"\nTotal de enlaces por URL: "+str(self.cloudSize.get()))
            self.cajaTexto.config(state=DISABLED)
            self.webMiner=WebMinerController(self.cloudSize.get(),self.algoritmo,self.query.get())
            self.progress=self.webMiner.getProgress()
            #self.webMiner.daemon=True            
            self.webMiner.start()
            thread.start_new_thread(self.barraProgreso,("",))
            thread.start_new_thread(self.crawlingProgress,("",))
            thread.start_new_thread(self.retrievalProgress,("",))
            thread.start_new_thread(self.scrapingProgress,("",))
        else:
            tkMessageBox.showwarning("ATENCION","Debe seleccionar un algoritmo !")

    def asignarEnfoquePonderado(self):self.algoritmo=self.enfoquePonderado
    def asignarCrank(self):self.algoritmo=self.cRank
    def asignarSupportVectorMachine(self):self.algoritmo=self.supportVectorMachine
    def asignarVectorial(self):self.algoritmo=self.modeloEspacioVectorial
    def asignarSemanticAnalysis(self):self.algoritmo=self.latentSemanticAnalysis

    def barraProgreso(self,var):
        #print "barra progresooo "
        self.boton.config(state=DISABLED)
	self.accion.set("Proceso:")
	barra=0
	while barra<=99:
            if barra!=99:
                time.sleep(0.01)
		self.progreso.set(str(barra)+'%')
		self.progressBar.step(1)
	    else:
		#time.sleep(0.5)
		self.progreso.set('100%')
		self.progressBar.step(0.99)
	    barra+=1
	self.boton.config(state=NORMAL)
	#print "Finalizado en "+str(barra)+"%"
 
    def crawlingProgress(self,var):
        self.accionCrawler.set('- Exploración de enlaces:')
        self.de.set('de')
        self.estadoCrawling.set(self.progress.get_crawlerState())
        self.totalCrawling.set(self.progress.get_totalCrawling())
        total=self.progress.get_totalCrawling()
        progreso=self.progress.get_crawlerProgress()
        while progreso<=total:
            self.estadoCrawling.set(self.progress.get_crawlerState())
            self.progresoCrawler.set(str(self.progress.get_crawlerProgress()))
            time.sleep(1)
            progreso=self.progress.get_crawlerProgress()


    def retrievalProgress(self,var):
        self.accionIR.set('- Ranking de documentos:')
        self.totalIR.set(self.progress.get_totalIR())
        progreso=self.progress.get_IRProgress()
        total=self.progress.get_totalIR()
        while progreso<=total:
            total=self.progress.get_totalIR()
            self.progresoIR.set(str(self.progress.get_IRProgress()))
            self.estadoIR.set(self.progress.get_IRState())
            self.totalIR.set(self.progress.get_totalIR())
            time.sleep(0.7)
            progreso=self.progress.get_IRProgress()

    
    def scrapingProgress(self,var):
        self.accionScraping.set('- Extacción de contenido:')
        while True:
            self.estadoScraping.set(self.progress.get_scrapingState())
            self.progresoScraping.set(str(self.progress.get_scrapingProgress()))
            self.totalScraping.set(self.progress.get_totalScraping())
            time.sleep(0.5)

root=Tk()
my_gui=GUI(root)
root.mainloop()

