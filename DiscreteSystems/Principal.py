'''Módulo desarrollado por Mauricio de Garay Hernández y Daniela Gómez Peniche
Fecha de entrega: 13/05/2020
En este módulo sirve como el controlador principal del programa en tiempo discreto
'''

import tkinter as tk
from FrameCoordenadas import FramePrincipal
from FuncionesVista import Funciones_V as Funciones

#Controlador
principal=tk.Tk()
principal.geometry=("800x800+100+0") #Definir la ventana
principal.resizable(False, False)
app = FramePrincipal(principal) #Creando una instncia de la clase FramePrincipal
principal.bind("<Return>", Funciones.MostrarResultados) #Si da enter muestra el resultado
principal.mainloop()