# !/usr/bin/env python3
# ## ###############################################
#
# guiApp.py
# Encargado de modificar los valores del gui (luces)
# 
# Autor : Luna Perez José Luis
#         Garcia Quezada Cristian Gabriel (deteccion y control timbre)
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

"""Function turned: In this function take a dicitionary, contains
information from the HTML about the lights, in this informations can see the status of
the switch and their grade of atenuation."""    
def turned(dic,GUI):
    GUI.Cambio_cocina(int(dic.get('cocina')))    
    GUI.Cambio_garage(int(dic.get('garage')))
    GUI.Cambio_pasillo(int(dic.get('pasillo')))
        
def detecciontimbre (dic, GUI):
    if dic.get("timbre")=='True':
        GUI.imgTimbre.setPixmap(QtGui.QPixmap("assets/timbreluz.png"))
        return True
    else:
        GUI.imgTimbre.setPixmap(QtGui.QPixmap("assets/timbreapag.png"))
        return False
        
def sonido (bool):
    if bool == True:
        time.sleep(3)
        playsound('timbre.mp3')
        print('playing sound using playsound')

def manejoPuertas(dic,GUI):
    if (dic.get("garage")=='False'):
        GUI.imgPuerta.setPixmap(QtGui.QPixmap("assets/garage.png"))
    else:
        GUI.imgPuerta.setPixmap(QtGui.QPixmap("assets/garageClose.png"))

def turnedOn(dic,GUI):
    if dic.get("cocina") == True:
        print("Aqui")
        GUI.Cambio_cocina(int(100))
    else:
        print("aqui no")
        GUI.Cambio_cocina(int(0))
        
    if dic.get("garage") == True:
        GUI.Cambio_garage(int(100))
    else:
        #print("entre 2")
        GUI.Cambio_garage(int(0))
        
    if dic.get("pasillo") == True:
        GUI.Cambio_pasillo(int(100))
    else:
        #print("Entre 3")
        GUI.Cambio_pasillo(int(0))
    
        
    
if __name__ == "__main__":
    dic = {'cocina': '20', 'cocina2': 'True', 'garage': '45', 'garage2':'False', 'pasillo': '10', 'pasillo2': 'False', 'timbre':'True'}
    dicPuertas ={'principal':'True','garage':'True'}
    app = QApplication(sys.argv)
    myWin = GUI_Main()
    turned(dic, myWin)
    print(int(myWin.pgb_pasillo.value()))
    print(int(myWin.pgb_garage.value()))
    print(int(myWin.pgb_cocina.value()))
    son = detecciontimbre(dic, myWin)
    manejoPuertas(dicPuertas, myWin)
    myWin.show()
    sonido(son)
    # turned(dic, myWin)
    # myWin.show()
    sys.exit(app.exec_())
