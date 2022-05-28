# !/usr/bin/env python3
# ## ###############################################
#
# interfaz.py
# Encargado de modificar los valores del gui (luces)
# 
# Autor : Luna Perez José Luis (luces)
#         Garcia Quezada Cristian Gabriel (deteccion y control timbre, y camaras de vigilancia)
#         Miranda Cortés Yak Balam
# License: MIT
#
# ## ###############################################
# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui_app import Ui_MainWindow

from playsound import playsound
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import cv2

"""GUI_Main Inicia la interfaz gráfica ademas de contener funciones que ocuparemos
en otras funciones."""
class GUI_Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(GUI_Main, self).__init__(parent)
        self.setupUi(self)
        self.pgb_garage.setValue(0)
        self.pgb_cocina.setValue(0)
        self.pgb_pasillo.setValue(0)
        
    def Cambio_cocina(self,x):
        self.pgb_cocina.setValue(x)
        
    def Cambio_garage(self,x):
        self.pgb_garage.setValue(x)
    
    def Cambio_pasillo(self,x):
        self.pgb_pasillo.setValue(x)
        
    def mouseReleaseEvent(self, *args, **kwargs):
        for widget in QApplication.topLevelWidgets():
            if type(widget) == GUI_Main:
                widget.close()

"""turned Encargada de poner el valor de las luces según lo recibido del Html."""    
def turned(dic,GUI):
    #Apartir de un valor entero proveniente del diccionario se cambiara el valor 
    #de la barra de progreso
    GUI.Cambio_cocina(int(dic.get('cocina')))    
    GUI.Cambio_garage(int(dic.get('garage')))
    GUI.Cambio_pasillo(int(dic.get('pasillo')))

"""detecciontimbre Recibe de un diccionario un valor booleano, una vez obtenido
cambiara la imagen que muestra que suena o no suena el timbre. Retorna un valor
booleano según el estatus del timbre."""        
def detecciontimbre (dic, GUI):
    if dic.get("timbre")==True:
        GUI.imgTimbre.setPixmap(QtGui.QPixmap("assets/timbreluz.png"))
        return True
    else:
        GUI.imgTimbre.setPixmap(QtGui.QPixmap("assets/timbreapag.png"))
        return False
    
"""sonido Recibe un valor booleano si es verdadero, el timbre fue tocado por lo cual
sonará."""        
def sonido (bool):
    if bool == True:
        playsound('timbre.mp3')
        print('playing sound using playsound')

"""manejoPuertas Recibe un diccionario, si algún valor valor es verdadero mostrara
una imagen de una puerta abierta, en caso contrario se cerrara."""        
def manejoPuertas(dic,GUI):
    if (dic.get("garage") == True):
        GUI.imgPuerta.setPixmap(QtGui.QPixmap("assets/garage.png"))
    else:
        GUI.imgPuerta.setPixmap(QtGui.QPixmap("assets/garageClose.png"))
    
    if (dic.get("principal") == True):
        GUI.imgPuerta_2.setPixmap(QtGui.QPixmap("assets/principalOpen.png"))
    else:
        GUI.imgPuerta_2.setPixmap(QtGui.QPixmap("assets/principalClose.png"))

"""turnedOn Recibira un diccionario con valores booleanos que nos dirán si la luz
esta encendida o no."""
def turnedOn(dic,GUI):
    if dic.get("cocina") == True:
        GUI.Cambio_cocina(int(100))
    else:
        GUI.Cambio_cocina(int(0))
        
    if dic.get("garage") == True:
        GUI.Cambio_garage(int(100))
    else:
        GUI.Cambio_garage(int(0))
        
    if dic.get("pasillo") == True:
        GUI.Cambio_pasillo(int(100))
    else:
        GUI.Cambio_pasillo(int(0))
        
"""lecturaIP Leera de un txt los valores de ip guardados."""
def lecturaIp():
    mensaje=[]
    with open("ip.txt") as archivo:
        for linea in archivo:
            mensaje.append(linea)
    return mensaje        

"""camaras Tomará el valor de una lista y tomara un valor de ip según corresponda 
a la camara seleccionada, eliminando los saltos de línea."""
def camaras(dic):
    ip=""
    url=""
    mensaje = lecturaIp()
    if dic.get("cam1") == True: 
        cad = mensaje[0].rstrip()
        vig(cad)
    elif dic.get("cam2") == True:
        cad = mensaje[0].rstrip()
        vig(cad)

"""vig Desplegara las camaras con el ip de la camara y se desplegarán gracias al 
paquete cv2."""
def vig(ip):
    url = "https://"+ip+":8080/video"
    try:
        capture = cv2.VideoCapture(url)
        while(True):
            _, frame = capture.read()
            cv2.imshow('videoc', frame)
            if cv2.waitKey(1) == ord("q"):
                break
        capture.release()
        cv2.destroyAllWindows()
    except Exception:
        print("Error: url incorrecta")
        
    
if __name__ == "__main__":
    dic = {'cocina': '20', 'cocina2': 'True', 'garage': '45', 'garage2':'False', 'pasillo': '10', 'pasillo2': 'False'}
    dicPuertas ={'principal':'True','garage':'True'}
    dicTimbre ={'timbre':'True'}
    dicCam ={'cam1':False,'cam2':True}
    app = QApplication(sys.argv)
    myWin = GUI_Main()
    turned(dic, myWin)
    print(int(myWin.pgb_pasillo.value()))
    print(int(myWin.pgb_garage.value()))
    print(int(myWin.pgb_cocina.value()))
    son = detecciontimbre(dicTimbre, myWin)
    manejoPuertas(dicPuertas, myWin)
    camaras(dicCam)
    myWin.show()
    sonido(son)
    # turned(dic, myWin)
    # myWin.show()
    sys.exit(app.exec_())
