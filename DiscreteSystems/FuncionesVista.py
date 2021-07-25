'''Módulo desarrollado por Mauricio de Garay Hernández y Daniela Gómez Peniche
Fecha de entrega: 13/05/2020
En este módulo se obtiene la información de la vista principal, se calculan, se grafican y se despliegan las respuestas del programa en tiempo discreto
'''

import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

#Modelo
class Funciones_V:
    x=0 
    y=0
    Opcion="Tache" #El default de seleccion es un polo, o tache
    VentanaActual="Coordenadas"
    ArregloPolos=[0,0,0,0,0]
    ArregloCeros=[0,0,0,0,0]
    ContadorPolos=0
    ContadorCeros=0
    numerador1=[]
    denominador1=[]
    Hz=""
    stringEc=""

    @staticmethod #hacer metodo estatico
    def MostrarResultados(OrigenEvento):
        if Funciones_V.VentanaActual=="Coordenadas":
            numerador=[]
            # tenemos H(z)=((1-C0z^-1)+....(1-Cnz^-1))/((1-P0z^-1)+....(1-Pnz^-1))
            #desarrolar numerador
            b=0 #bandera del numerador
            if Funciones_V.ContadorCeros==0:
                numerador.append(1) #Si no hay ceros el numerador es 1
                b=1
            if Funciones_V.ContadorCeros==1:
                numerador=[1,-1*Funciones_V.ArregloCeros[0]] #numerador si hay un cero
                b=2
            if Funciones_V.ContadorCeros==2: #Numerador si hay dos ceros
                N0=np.convolve([1, -1*Funciones_V.ArregloCeros[0]], [1, -1*Funciones_V.ArregloCeros[1]])
                numerador=N0
                b=3
            if Funciones_V.ContadorCeros==3: #Numerador si hay tres ceros
                N0=np.convolve([1, -1*Funciones_V.ArregloCeros[0]], [1, -1*Funciones_V.ArregloCeros[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloCeros[2]])
                numerador=N1
                b=4
            if Funciones_V.ContadorCeros==4: #Numerador si hay cuatro ceros
                N0=np.convolve([1, -1*Funciones_V.ArregloCeros[0]], [1, -1*Funciones_V.ArregloCeros[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloCeros[2]])
                N2=np.convolve(N1, [1, -1*Funciones_V.ArregloCeros[3]])
                numerador=N2
                b=5
            if Funciones_V.ContadorCeros==5: #Numerador si hay cinco ceros
                N0=np.convolve([1, -1*Funciones_V.ArregloCeros[0]], [1, -1*Funciones_V.ArregloCeros[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloCeros[2]])
                N2=np.convolve(N1, [1, -1*Funciones_V.ArregloCeros[3]])
                N3=np.convolve(N2, [1, -1*Funciones_V.ArregloCeros[4]])
                numerador=N3
                b=6
            numerador=np.around(numerador,6)
            #Lo mismo pero con denominador
            denominador=[]
            b1=0 #bandera del denominador
            if Funciones_V.ContadorPolos==0:
                denominador.append(1) #si no hay polos, el denominador es uno
                b1=1
            if Funciones_V.ContadorPolos==1:
                denominador=[1,-1*Funciones_V.ArregloPolos[0]] #denominador si hay un polo
                b1=2
            if Funciones_V.ContadorPolos==2: #denominadr si hay dos polos
                N0=np.convolve([1, -1*Funciones_V.ArregloPolos[0]], [1, -1*Funciones_V.ArregloPolos[1]])
                denominador=N0
                b1=3
            if Funciones_V.ContadorPolos==3: #denominador si hay tres polos
                N0=np.convolve([1, -1*Funciones_V.ArregloPolos[0]], [1, -1*Funciones_V.ArregloPolos[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloPolos[2]])
                denominador=N1
                b1=4
            if Funciones_V.ContadorPolos==4: #denominador si hay cuatro polos
                N0=np.convolve([1, -1*Funciones_V.ArregloPolos[0]], [1, -1*Funciones_V.ArregloPolos[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloPolos[2]])
                N2=np.convolve(N1, [1, -1*Funciones_V.ArregloPolos[3]])
                denominador=N2
                b1=5
            if Funciones_V.ContadorPolos==5: #denominador si hay cinco polos
                N0=np.convolve([1, -1*Funciones_V.ArregloPolos[0]], [1, -1*Funciones_V.ArregloPolos[1]])
                N1=np.convolve(N0, [1, -1*Funciones_V.ArregloPolos[2]])
                N2=np.convolve(N1, [1, -1*Funciones_V.ArregloPolos[3]])
                N3=np.convolve(N2, [1, -1*Funciones_V.ArregloPolos[4]])
                denominador=N3
                b1=6
            denominador=np.around(denominador,6) #redondear para que no se vea tan feo
            print(denominador)
            ventana2=tk.Tk()
            #ya tenemos la funcion de transferencia
            stringHz="H(z)=\\frac{"
            i=0
            #Hacer el string de la funcion de transferencia
            if b==1:
                stringNum="1}{"   
                stringHz=stringHz+stringNum
            #if b==2:
                #stringNum="1-{}z^-1)/(".format(numerador[0])
                #stringHz=stringHz+stringNum
            if b>1:
                stringNum=""
                while i<numerador.size:
                    if i==numerador.size-1: #Si es mi ultimo valor del numerados
                        aux="{}z^".format(np.real(numerador[i]))
                        aux=aux+"{"
                        aux=aux+"-{}".format(i)
                        aux=aux+"}}{"
                        stringNum=stringNum+aux
                    else: #Si no es mi ultimo valor del numerador
                        aux="{}z^".format(np.real(numerador[i]))
                        aux=aux+"{"
                        aux=aux+"-{}".format(i)
                        aux=aux+"}+"
                        stringNum=stringNum+aux
                    i=i+1
                stringHz=stringHz+stringNum
            i=0
            if b1==1:
                stringDenom="1}" #Si el numerador es uno
                stringHz=stringHz+stringDenom
            #if b1==2:
                #stringDenom="1-{}z^-1)".format(denominador[0])
                #stringHz=stringHz+stringDenom
            if b1>1:
                stringDenom=""
                while i<denominador.size:
                    if i==denominador.size-1: #Si esta en el ultimo valor del denominador
                        aux="{}z^".format(np.real(denominador[i]))
                        aux=aux+"{"
                        aux=aux+"-{}".format(i)
                        aux=aux+"}}"
                        stringDenom=stringDenom+aux
                    else: #Si no esta en el ultimo valor del denominador
                        aux="{}z^".format(np.real(denominador[i]))
                        aux=aux+"{"
                        aux=aux+"-{}".format(i)
                        aux=aux+"}+"
                        stringDenom=stringDenom+aux
                    i=i+1
                stringHz=stringHz+stringDenom

            #Ya sabemos la ecuacion de diferencias.
            Funciones_V.Hz=stringHz
            BotonHz=tk.Button(ventana2, text="Ver H(z)", command=Funciones_V.VerHz)
            BotonHz.pack()
            stringEc="" #String de la ecuacion de diferencias
            i=0
            if b1==1:
                stringY="y[n]=" #Si el denominador es uno
                stringEc=stringEc+stringY
            #if b1==2:
                #stringY="y[n]+{}y[n-1]=".format(denominador[0])
                #stringEc=stringEc+stringY
            if b1>1:
                stringY=""
                while i<denominador.size:
                    if i==denominador.size-1:
                        aux="{}y[n-{}]=".format(np.real(denominador[i]),(i))
                        stringY=stringY+aux
                    else:
                        aux="{}y[n-{}]+".format(np.real(denominador[i]),(i))
                        stringY=stringY+aux
                    i=i+1
                stringEc=stringEc+stringY
            i=0
            if b==1:
                stringX="x[n]"   
                stringEc=stringEc+stringX
            #if b==2:
                #stringX="x[n]+{}x[n-1]".format(numerador[0])
                #stringEc=stringEc+stringX
            if b>1:
                stringX=""
                while i<numerador.size:
                    if i==numerador.size-1:
                        aux="{}x[n-{}]".format(np.real(numerador[i]),(i))
                        stringX=stringX+aux
                    else:
                        aux="{}x[n-{}]+".format(np.real(numerador[i]),(i))
                        stringX=stringX+aux
                    i=i+1
                stringEc=stringEc+stringX
            
            Funciones_V.stringEc=stringEc
            BotonEc=tk.Button(ventana2,text="Ver ecuación de diferencias.", command=Funciones_V.VerEcuacion)
            BotonEc.pack()

            #Ahora hay que obtener los coeficientes por fraccion parcial
            CajaR=tk.Frame(master=ventana2) #Caja para las graficas del resultado
            CajaR.pack()
            t=np.arange(0,40, 1)
            h=np.zeros(40)
            if not(numerador.size>1 and denominador.size==1 and denominador[0]==1):
                r,p,k=signal.residuez(numerador, denominador) #r=coeficientes, p=polos, k=constante si no es f. parcial
                print("Coeficientes:", r)
                print("Polos: ", p)
                print("Constante: ", k)
                #Obtenemos duración respuesta al impulso
                Duracion=100000
                for polo in Funciones_V.ArregloPolos:
                    absoluto=np.abs(polo)
                    if np.abs(1-absoluto)<Duracion:
                        Duracion=absoluto
                if Duracion==0:
                    Duracion=10
                else:
                    print(Duracion)
                    Duracion=int(5/Duracion)
                
                for rr,pp in zip(r,p):
                    h=h+rr*pp**t #forma de h[n]
                for kk in k: #Si sobra una constante
                        h[0]=h[0]+kk #La transformada inversa de kk es kk por un impulso
            else: #Si solo hay ceros y no hay polos, la transformada inversa de h(z) son impulsos retrasados.
                i=0
                for n in numerador:
                    h[i]=n
                    i=i+1
                Duracion=numerador.size+1
            #Graficar y meterlo a la caja, ademas agregar slider de n para elegir cuántas muestras ver
            f = plt.Figure()
            eje=f.add_subplot(111,title="h[n] (y) vs n [x]")
            eje.stem(t,h, use_line_collection=True)
            eje.set_xlim(-0.2,Duracion+0.2)
            eje.grid()
            caja1=tk.Frame(master=CajaR)
            labelt=tk.Label(caja1, text="Respuesta al impulso(usa slider para ajustar número de muestras): ")
            labelt.pack()
            caja1.pack(side=tk.LEFT)
            canvas = FigureCanvasTkAgg(f, master=caja1)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            eje_hor=f.add_axes([0.12,0.1,0.78,0.03]) #Delimitar el eje del slider
            s_hor=Slider(eje_hor,'Num Muestras',2, 40,valinit=Duracion, valstep=1) #Crear el slider
            #Función cuando el slider es utilizado
            def update(val): 
                pos=int(s_hor.val)
                eje.set_xlim(-0.2,pos+0.2)
                f.canvas.draw_idle()
            s_hor.on_changed(update)
            #Opciones de la grafica
            toolbar = NavigationToolbar2Tk(canvas, caja1)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


            

            
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

           #respuesta al escalón, multiplicando H(z)*(1/1-z^-1) y haciendo fracciones parciales y transformada invesa
            suma=0
            sn=np.zeros(t.size)
            #Fracciones parciales
            r,p,k=signal.residuez(numerador, np.convolve(denominador,[1,-1]))
            #Transformada inversa
            for rr,pp in zip(r,p):
                sn=sn+ rr*pp**t
            for kk in k:
                sn[0]=sn[0]+kk
            

            #Graficar la respuesta al escalon más slider para elegir muestras que ver
            f1 = plt.Figure()
            eje1=f1.add_subplot(111, title="S[n] (y) vs n [x]")
            eje1.stem(t,sn,use_line_collection=True)
            eje1.set_xlim(-0.2, Duracion+0.2)
            eje1.grid()
            caja=tk.Frame(master=CajaR)
            labelsn=tk.Label(caja, text="Respuesta al escalón(usa slider para ajustar número de muestras):")
            labelsn.pack()
            caja.pack(side=tk.RIGHT)
            canvas2 = FigureCanvasTkAgg(f1, master=caja)  # A tk.DrawingArea.
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            toolbar2 = NavigationToolbar2Tk(canvas2, caja)
            toolbar2.update()
            canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
            eje_hor1=f1.add_axes([0.12,0.1,0.78,0.03]) #Delimitar el eje del slider
            s_hor1=Slider(eje_hor1,'Num. Muestras',2, 40,valinit=Duracion, valstep=1) #Crear el slider
            #Función cuando el slider es utilizado
            def update1(val): 
                pos=int(s_hor1.val)
                eje1.set_xlim(-0.2,pos+0.2)
                f1.canvas.draw_idle()
            s_hor1.on_changed(update1)
            Funciones_V.numerador1=numerador #igualar las variables estaticas a las locales
            Funciones_V.denominador1=denominador
            #Boton para obtener la respuesta en frecuencia
            botonF=tk.Button(master=ventana2, text="Respuesta en Frecuencia", command= Funciones_V.VerRespuestaF)
            botonF.pack()
            
            ventana2.mainloop()
            Funciones_V.VentanaActual="Resultados"
        else:
            exit()
    @staticmethod
    def VerHz():
        #Ajustar tamaño de letra dependiendo tamaño de numerador/denominador y coeficientes
        font=25
        inicioX=0.2
        if Funciones_V.numerador1.size>3:
            font=18
            inicioX=0
        for rr in Funciones_V.numerador1:
            if np.abs(rr)>1000:
                font=18
                inicioX=0
            if np.abs(rr)>10000:
                font=15
                inicioX=0
            if np.abs(rr)>100000:
                font=10
                inicioX=0
        if Funciones_V.denominador1.size>3:
            font=18
            inicioX=0
        for rr in Funciones_V.denominador1:
            if np.abs(rr)>1000:
                font=18
                inicioX=0
            if np.abs(rr)>10000:
                font=15
                inicioX=0
            if np.abs(rr)>100000:
                font=10
                inicioX=0
        ventana=tk.Tk()
        label = tk.Label(ventana)
        label.pack()
        ventana.geometry("1300x800")
        fig = Figure(figsize=(20, 20), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=label)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        texto="$"+Funciones_V.Hz+"$"
        ax.clear()
        ax.text(inicioX, 0.6, texto, fontsize = font)  
        canvas.draw()
    @staticmethod
    def VerEcuacion():
        #Ajustar tamaño de letra dependiendo tamaño de coeficientes
        font=18
        inicioX=0.2
        if Funciones_V.numerador1.size>3:
            font=10
            inicioX=0
        for rr in Funciones_V.numerador1:
            if np.abs(rr)>1000:
                font=15
                inicioX=0
            if np.abs(rr)>10000:
                font=10
                inicioX=0
            if np.abs(rr)>100000:
                font=8.35
                inicioX=0
        if Funciones_V.denominador1.size>3:
            font=10
            inicioX=0
        for rr in Funciones_V.denominador1:
            if np.abs(rr)>1000:
                font=15
                inicioX=0
            if np.abs(rr)>10000:
                font=10
                inicioX=0
            if np.abs(rr)>100000:
                font=8.35
                inicioX=0
        ventana=tk.Tk()
        label = tk.Label(ventana)
        label.pack()
        ventana.geometry("1300x800")
        fig = Figure(figsize=(20, 20), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=label)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        #Separar lado x de lado y para que uno este por encima del otro y tener mejor formato
        t1=Funciones_V.stringEc.split("=")
        texto="$"+t1[0]+"="+"$\n"+"$"+t1[1]+"$"
        ax.clear()
        ax.text(inicioX, 0.6, texto, fontsize = font)  
        canvas.draw()
    @staticmethod
    def VerRespuestaF():
        numerador=Funciones_V.numerador1
        denominador=Funciones_V.denominador1
        #Ahora hay que obtener la respuesta en frecuencia
        ventana3=tk.Tk()
        CajaF=tk.Frame(master=ventana3)
        CajaF.pack()
        w=np.linspace(np.pi*-1,np.pi,300)
        #Por los exponentes negativos necesito voltear los coeficientes del numerador y denominador para poder evaluar en polyval en 1/x^n
        a=[]
        i=numerador.size-1
        b=[]
        while i>=0:
            b.append(numerador[i])
            i=i-1
        i=denominador.size-1
        while i>=0:
            a.append(denominador[i])
            i=i-1
        print(denominador)
        print(a)
        #si el numerador va desde z^-1 hasta z^-n, b va a ser= CNz^-n +CNz^-n-1+.... C1z^-1. Lo mismo con el denominador
        #ya los voltee, ahora puedo evaluar en 1/e^jw (porque es exponente negativo)
        Caja1=tk.Frame(master=CajaF)
        Caja1.pack(side=tk.LEFT)
        H=np.polyval(b, 1/np.exp(1j*w))/np.polyval(a, 1/np.exp(1j*w))

        #Graficas respuesta en frecuencia
        f2 = plt.Figure()
        eje1=f2.add_subplot(111, xlabel="Frecuecia", ylabel="Amplitud", title="Frecuencia (x) vs Amplitud (y)")
        eje1.plot(w, np.abs(H))
        eje1.grid()
        labelF=tk.Label(Caja1, text="Respuesta en Frecuencia Amplitud:")
        labelF.pack()
        canvas3 = FigureCanvasTkAgg(f2, master=Caja1)  # A tk.DrawingArea.
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        toolbar3 = NavigationToolbar2Tk(canvas3, Caja1)
        toolbar3.update()
        canvas3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        Caja2=tk.Frame(master=CajaF)
        Caja2.pack(side=tk.RIGHT)
        labelFase=tk.Label(Caja2, text="Respuesta en Frecuencia Fase:")
        labelFase.pack()
        f3 = plt.Figure()
        eje2=f3.add_subplot(111, xlabel="Fase", ylabel="Frecuencia", title="Frecuencia (x) vs Fase (y)")
        eje2.plot(w, np.angle(H)/np.pi)
        eje2.grid()
        canvas4 = FigureCanvasTkAgg(f3, master=Caja2)  # A tk.DrawingArea.
        canvas4.draw()
        canvas4.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        toolbar4 = NavigationToolbar2Tk(canvas4, Caja2)
        toolbar4.update()
        canvas4.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        ventana3.title("Respuesta en Frecuencia")
        ventana3.mainloop()
    @staticmethod
    def BotonCeroClick():
         Funciones_V.Opcion="Corazon" #Cambiar la variable a corazon, para colocar ceros
         print("Cora")
    @staticmethod
    def BotonPoloClick():
         Funciones_V.Opcion="Tache" #Cambiar la variable a tache, para colocar polos
         print("Tache")




