'''Módulo desarrollado por Mauricio de Garay Hernández y Daniela Gómez Peniche
Fecha de entrega: 13/05/2020
En este módulo se desarrolla la vista principal de la interfaz con el usuario en discreto
'''

import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk
from FuncionesVista import Funciones_V as F
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

import matplotlib.image as mpimg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.widgets import Slider, Button

from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from tkinter import ttk

#Vista
class FramePrincipal:
    x=0
    y=0
    ListaImagenes=[]
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master=self.master)
        self.frame.config(height=800, width=800)
        self.Canvas=tk.Canvas(self.frame, width=800, height=800)
        self.Canvas.pack()
        self.BotonCoordenadas=tk.Button(master=self.Canvas,text="Elegir", command=self.AgregarCoordenada)
        self.label=tk.Label(master=self.Canvas, text="Ingresar coordenadas exactas:")
        self.label.place(x=600, y=20)
        self.TextoReal=tk.Spinbox(master=self.Canvas,from_=0, to=5, increment=0.0001, width=6)
        self.TextoReal.place(x=600,y=40)
        self.labelmas=tk.Label(master=self.Canvas, text="+")
        self.labelmas.place(x=660, y=40)
        self.TextoImaginario=tk.Spinbox(master=self.Canvas,from_=0, to=5, increment=0.0001, width=6)
        self.TextoImaginario.place(x=680, y=40)
        self.labelj=tk.Label(master=self.Canvas, text="j")
        self.labelj.place(x=730, y=40)
        self.BotonCoordenadas.place(x=730, y=60)
        self.labelTolerancia=tk.Label(self.Canvas, text="Tolerancia Reales (%).")
        self.labelTolerancia.place(x=650, y=360)
        self.TextoTolerancia=ttk.Combobox(self.Canvas, values=["1","2","3","4","5"])
        self.TextoTolerancia.place(x=650, y=380)
        self.TextoTolerancia.current(3)
        self.zoomout=tk.Button(master=self.Canvas, text="Zoom Out", command=self.ZoomOut)
        self.zoomout.place(x=675, y=420)
        self.zoomin=tk.Button(master=self.Canvas, text="Zoom In", command=self.ZoomIn)
        self.zoomin.place(x=675, y=450)
        self.Borrar=tk.Button(master=self.Canvas, text="Borrar Polos y Ceros", command=self.BorrarTodo)
        self.Borrar.place(x=675, y=480)
        self.Reset=tk.Button(master=self.Canvas, text="Reset Posicion", command=self.ResetPosicion)
        self.Reset.place(x=675, y=510)
        #grafica
        matplotlib.use("TkAgg")
        self.f = plt.Figure()
        self.caja1=tk.Frame(master=self.Canvas)
        self.caja1.place(x=0, y=100)
        self.canvas = FigureCanvasTkAgg(self.f, master=self.caja1)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1) 
        Real=np.arange(-5, 5, 100000)
        Imag=np.arange(-5, 5, 100000)
        self.eje=self.f.add_subplot(111)
        self.eje.set_ylabel("Imaginario")
        self.eje.set_xlabel("Real")
        self.eje.plot()
        self.f.subplots_adjust(bottom=0.25)
        #Círculo unitario
        circ = plt.Circle((0, 0), radius=1, edgecolor='black', facecolor='None')
        self.eje.add_patch(circ)
        self.eje.grid(which="major", alpha=0.5)
        self.eje.grid(which="minor")
        self.eje.set_ylim(-1,1)
        self.eje.set_xlim(-1,1)#Limites de los self.ejes
        self.eje.axhline() #Crear una linea en el self.eje horizontal
        self.eje.axvline() #Crear una linea en el self.eje verticals
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.caja1)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        #si hace click en una coordenada
        self.f.canvas.mpl_connect('button_press_event', self.onclick)
        #Botones Ceros y Polos
        self.im1=Image.open("Corazon.jpg")
        newsize=(10,10)
        self.im1=self.im1.resize(newsize)
        self.ph1=ImageTk.PhotoImage(self.im1)
        self.im2=Image.open("TACHE.jpg")
        newsize=(10,10)
        self.im2=self.im2.resize(newsize)
        self.ph2=ImageTk.PhotoImage(self.im2)
        self.BotonCero=tk.Button(master=self.Canvas, text="Ceros", image=self.ph1, compound=tk.LEFT, command=F.BotonCeroClick)
        self.BotonCero.place(x=10,y=20)
        self.BotonPolo=tk.Button(master=self.Canvas, text="Polos", image=self.ph2, compound=tk.LEFT, command=F.BotonPoloClick)
        self.BotonPolo.place(x=10,y=50)
        self.Label=tk.Label(master=self.Canvas, text="Presiona <enter> para ver resultados")
        self.Label.place(x=300, y=30)
        self.Instrucciones=tk.Label(master=self.Canvas, text="Utilice doble click para seleccionar coordenada.")
        self.Instrucciones.place(x=300, y=5)
        self.BotonAyuda=tk.Button(master=self.Canvas,text="Ver instrucciones gráfica.", command=self.verAyuda, bg="#daf5f4")
        self.BotonAyuda.place(x=300, y=50)
        self.frame.pack()



    #Boton Ayuda
    def verAyuda(evento):
        messagebox.showinfo("Ayuda Gráfica", "La gráfica funciona de la siguiente manera:\n-Se selecciona una coordenada con doble click, si es compleja en automático se pone su conjugado. Para poner reales con precisión se agrega una tolerancia a través de la combobox, donde el valor elegido es el porcentaje de tolerancia que tendrá el eje Imaginario para seleccionar valores reales. El programa redondea a 6 dígitos.\n-También puedes ingresar coordenadas de manera exacta con las spinboxes de la esquina superior derecha, y es la manera recomendada para ingresar valores reales/valores con mayor precisión.\n-Las opciones de la gráfica son con un solo click.\n-Para elegir entre polos y ceros, da click en el botón de tu preferencia en la esquina superior izquierda de la ventana.\n-La opción de la lupa te permite hacer zoom en una región rectangular que selecciones, se puede hacer multiples veces.\n-Las imágenes de los polos y ceros se ponen en la coordenada (x,y) de la gráfica que representa (no dependen de pixeles), puedes hacer zoom a esta región para verlas más de cerca, o alejarte de la región para no verlas más.\n-Si deseas resetear la posición de la gráfica, presiona el botón de la casa. Si es que por alguna razón una imágen de polos o ceros no aparece, puedes útilizar este botón y/o el zoom para actualizarla.\n-Los sliders funcionan para moverte rápidamente a algún valor de la gráfica.\n-Se asume que los sistemas parten del reposo, y se valida que tengan estabilidad BIBO.\n-La magnitud/valor absoluto máximo que puede tener un polo o cero es de 5.\n-Zoom out incrementa márgenes XY +1 (Ej: máximo x pasa de 1 a 2), Zoom in lo divide 10 veces si son 1 o menos, y les resta 1 si son mayores a 1 (Ej: máximo x pasa de 1 a 0.1, o máximo x pasa de 4 a 3).\n-Reset Posición regresa la escala a 1x1.\n-Borrar Polos y Ceros borra los polos y los ceros de la gráfica y de arreglo de polos y ceros.\n-Se calcula automáticamente la duración de la respuesta al impulso con base en el valor absoluto de los polos. Además, se agregan sliders para ver la respuesta en diferentes duraciones de muestras.\n-La gráfica de frecuencia va de -pi a pi y los valores de fase son fracciones de pi.")
    #Boton Borrar
    def BorrarTodo(self):
        
        for imagen in FramePrincipal.ListaImagenes:
            imagen.remove()
        FramePrincipal.ListaImagenes=[]
        F.ContadorPolos=0
        F.ContadorCeros=0
        F.ArregloPolos=[0,0,0,0,0]
        F.ArregloCeros=[0,0,0,0,0]
        self.f.canvas.draw_idle()
    #Boton Reset
    def ResetPosicion(self):
        self.eje.set_xlim(-1,1)
        self.eje.set_ylim(-1,1)
        self.f.canvas.draw_idle()
    #Métodos Gráfica
    def ZoomOut(self):
        LimiteInferiorY, LimiteSuperiorY=self.eje.get_ylim()
        LimiteInferiorX, LimiteSuperiorX=self.eje.get_xlim()
        NuevoX=LimiteSuperiorX+1
        NuevoY=LimiteSuperiorY+1
        if NuevoX>5 or NuevoY>5:
            self.eje.set_xlim(-5,5)
            self.eje.set_ylim(-5,5)
        else:
            self.eje.set_xlim(NuevoX*-1,NuevoX)
            self.eje.set_ylim(NuevoY*-1,NuevoY)
        self.f.canvas.draw_idle()
    def ZoomIn(self):
         LimiteInferiorY, LimiteSuperiorY=self.eje.get_ylim()
         
         LimiteInferiorX, LimiteSuperiorX=self.eje.get_xlim()
         NuevoX=0
         NuevoY=0
         if np.absolute(LimiteInferiorX)>1 and np.absolute(LimiteSuperiorX)>1 and np.absolute(LimiteInferiorY)>1 and np.absolute(LimiteSuperiorY)>1:
             NuevoX=LimiteSuperiorX-1
             NuevoY=LimiteSuperiorY-1
         else:
             NuevoX=LimiteSuperiorX/10
             NuevoY=LimiteSuperiorY/10
         if NuevoY<1e-4 or NuevoX<1e-4:
             messagebox.showerror("Limites Excedidos", "ERROR: no puedes hacer más zoom in.")
             return
         self.eje.set_xlim(NuevoX*-1,NuevoX)
         self.eje.set_ylim(NuevoY*-1,NuevoY)
         self.f.canvas.draw_idle()
    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
        if event.dblclick:
            porcentaje=float(self.TextoTolerancia.get())
            porcentaje=porcentaje/100
            print(porcentaje)
            LimiteInferior, LimiteSuperior=self.eje.get_ylim()
            Tolerancia=LimiteSuperior-LimiteInferior
            Tolerancia=Tolerancia*porcentaje
            if LimiteInferior>0:
                Tolerancia=0
            FramePrincipal.x=event.xdata
            FramePrincipal.y=event.ydata
            FramePrincipal.x=round(FramePrincipal.x, 3)
            FramePrincipal.y=round(FramePrincipal.y, 3)
            valorImaginario=FramePrincipal.y
            ValorComplejo= FramePrincipal.x + FramePrincipal.y*1j
            if valorImaginario>=(Tolerancia*-1) and valorImaginario <=Tolerancia: #Generar tolerancia para que sea más fácil colocar un real
                valorImaginario=0
            ValorComplejo= FramePrincipal.x + valorImaginario*1j
            #Validaciones
            if np.abs(ValorComplejo)>5:
                messagebox.showerror("Valor absoluto mayor a 1x10^6", "ERROR: el valor absoluto del numero debe ser <=5")
                return
            ComplejoConjugado= FramePrincipal.x - FramePrincipal.y*1j
            if F.Opcion=="Tache":
                if F.ContadorPolos>4:
                      messagebox.showerror("Numero Excedido", "ERROR: solo se permiten 5 polos máximo.")
                      return
                if np.abs(ValorComplejo)>=1:
                    messagebox.showerror("Estabilidad", "ERROR: Este valor no permite estabilidad BIBO en el sistema")
                    return
                print("a")
                imgT=Image.open("TACHE.jpg")
                newsize=(10,10)
                imgT=imgT.resize(newsize)
                imagebox = OffsetImage(imgT, zoom=1)
                if  valorImaginario!=0:
                    if F.ContadorPolos>=4:
                        messagebox.showerror("Numero Excedido", "ERROR: Los polos seran más de 5. Ingresa un polo real.")
                        return
                    F.ArregloPolos[F.ContadorPolos]=ValorComplejo
                    F.ArregloPolos[F.ContadorPolos+1]=ComplejoConjugado
                    F.ContadorPolos=F.ContadorPolos+2
                else:
                    F.ArregloPolos[F.ContadorPolos]=np.real(ValorComplejo)
                    F.ContadorPolos=F.ContadorPolos+1
            if F.Opcion=="Corazon":
                if F.ContadorCeros>4:
                    messagebox.showerror("Numero Excedido", "ERROR: solo se permiten 5 ceros máximo.")
                    return
                imgC=Image.open("Corazon.jpg")
                newsize=(10,10)
                imgC=imgC.resize(newsize)
                imagebox = OffsetImage(imgC, zoom=1)
                if valorImaginario!=0:
                    if F.ContadorCeros>=4:
                        messagebox.showerror("Numero Excedido", "ERROR: Los ceros seran más de 5. Ingresa un cero real.")
                        return
                    F.ArregloCeros[F.ContadorCeros]=ValorComplejo
                    F.ArregloCeros[F.ContadorCeros+1]=ComplejoConjugado
                    F.ContadorCeros=F.ContadorCeros+2
                else:
                    F.ArregloCeros[F.ContadorCeros]=np.real(ValorComplejo)
                    F.ContadorCeros=F.ContadorCeros+1
            i=0
            print("Ceros: ")
            while i<5:
                print(F.ArregloCeros[i])
                i=i+1
            i=0
            print("Polos: ")
            while i<5:
                print(F.ArregloPolos[i])
                i=i+1
            #Si son complejas, poner ambos polos
            if valorImaginario!=0:
                ab = AnnotationBbox(imagebox, (FramePrincipal.x, FramePrincipal.y))
                ab2=AnnotationBbox(imagebox, (FramePrincipal.x, FramePrincipal.y*-1))
                self.eje.add_artist(ab)
                self.eje.add_artist(ab2)
                FramePrincipal.ListaImagenes.append(ab)
                FramePrincipal.ListaImagenes.append(ab2)
            else:
                 ab = AnnotationBbox(imagebox, (FramePrincipal.x, 0))
                 self.eje.add_artist(ab)
                 FramePrincipal.ListaImagenes.append(ab)
            self.f.canvas.draw()
    #Método Ingresar Coordenadas Manualmente
    def AgregarCoordenada(self):
        try:
            valorReal=float(self.TextoReal.get())
            valorImaginario=float(self.TextoImaginario.get())
            ValorComplejo=valorReal + valorImaginario*1j    
        except: #Validaciones
            messagebox.showerror("Dato invalido", "ERROR: solo se permiten valores numéricos.")
            return
        if np.abs(ValorComplejo)>5:
            messagebox.showerror("Valor absoluto mayor a 5", "ERROR: el valor absoluto del numero debe ser <=5")
            return
        ComplejoConjugado=valorReal - valorImaginario*1j
        if F.Opcion=="Tache":
            if F.ContadorPolos>4:
                  messagebox.showerror("Numero Excedido", "ERROR: solo se permiten 5 polos máximo.")
                  return
            if np.abs(ValorComplejo)>=1:
                messagebox.showerror("Estabilidad", "ERROR: Este valor no permite estabilidad BIBO en el sistema")
                return
                    
            imgT=Image.open("TACHE.jpg")
            newsize=(10,10)
            imgT=imgT.resize(newsize)
            imagebox = OffsetImage(imgT, zoom=1)
            if  valorImaginario!=0:
                if F.ContadorPolos>=4:
                    messagebox.showerror("Numero Excedido", "ERROR: Los polos seran más de 5. Ingresa un polo real.")
                    return
                F.ArregloPolos[F.ContadorPolos]=ValorComplejo
                F.ArregloPolos[F.ContadorPolos+1]=ComplejoConjugado
                F.ContadorPolos=F.ContadorPolos+2
            else:
                F.ArregloPolos[F.ContadorPolos]=np.real(ValorComplejo)
                F.ContadorPolos=F.ContadorPolos+1
        if F.Opcion=="Corazon":
            if F.ContadorCeros>4:
                messagebox.showerror("Numero Excedido", "ERROR: solo se permiten 5 ceros máximo.")
                return
            imgC=Image.open("Corazon.jpg")
            newsize=(10,10)
            imgC=imgC.resize(newsize)
            imagebox = OffsetImage(imgC, zoom=1)
            if valorImaginario!=0:
                if F.ContadorCeros>=4:
                    messagebox.showerror("Numero Excedido", "ERROR: Los ceros seran más de 5. Ingresa un cero real.")
                    return
                F.ArregloCeros[F.ContadorCeros]=ValorComplejo
                F.ArregloCeros[F.ContadorCeros+1]=ComplejoConjugado
                F.ContadorCeros=F.ContadorCeros+2
            else:
                F.ArregloCeros[F.ContadorCeros]=np.real(ValorComplejo)
                F.ContadorCeros=F.ContadorCeros+1
        i=0
        print("Ceros: ")
        while i<5:
            print(F.ArregloCeros[i])
            i=i+1
        i=0
        print("Polos: ")
        while i<5:
            print(F.ArregloPolos[i])
            i=i+1
        #Si son complejas, poner ambos polos
        if valorImaginario!=0:
            ab = AnnotationBbox(imagebox, (valorReal, valorImaginario))
            ab2=AnnotationBbox(imagebox, (valorReal, valorImaginario*-1))
            self.eje.add_artist(ab)
            self.eje.add_artist(ab2)
            FramePrincipal.ListaImagenes.append(ab)
            FramePrincipal.ListaImagenes.append(ab2)
        else:
            ab = AnnotationBbox(imagebox, (valorReal, 0))
            self.eje.add_artist(ab)
            FramePrincipal.ListaImagenes.append(ab)
        self.f.canvas.draw()


        


    
    
