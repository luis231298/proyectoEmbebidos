# !/usr/bin/env python3
# ## ###############################################
#
# LUPL_webserver.py
# Starts a custom webserver and handles all requests
#
# Autor: José Luis Luna Pérez
# Original by: Mauricio Matamoros
# License: MIT
#
# ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import json
import magic
from http.server import BaseHTTPRequestHandler, HTTPServer
from interfaz import detecciontimbre, sonido, GUI_Main, turnedOn, turned, manejoPuertas, camaras
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui_app import Ui_MainWindow

# Nombre o dirección IP del sistema anfitrión del servidor web
address = "192.168.56.1"
# Puerto en el cual el servidor estará atendiendo solicitudes HTTP
# El default de un servidor web en produción debe ser 80
port = 80#puerto a usar

class WebServer(BaseHTTPRequestHandler):
    """Sirve cualquier archivo encontrado en el servidor"""
    def _serve_file(self, rel_path):
        if not os.path.isfile(rel_path):
            self.send_error(404)
            return
        self.send_response(200)
        mime = magic.Magic(mime=True)
        self.send_header("Content-type", mime.from_file(rel_path))
        self.end_headers()
        with open(rel_path, 'rb') as file:
            self.wfile.write(file.read())
    
    """Sirve el archivo de interfaz de usuario"""
    def _serve_ui_file(self):
        if not os.path.isfile("index.html"):
            err = "index.html not found."
            self.wfile.write(bytes(err, "utf-8"))
            print(err)
            return
        try:
            with open("index.html", "r") as f:
                content = "\n".join(f.readlines())
        except:
            content = "Error reading index.html"
        self.wfile.write(bytes(content, "utf-8"))
        
    """_parse_post encargada de obtener el json y obtener las llaves  que contiene
    el json, una vez obtenidas guardara en un diccionario para ser mandados a interfaz.py
    donde se ejecuta lo relacionado a la interfaz y camaras"""
    def _parse_post(self, json_obj):
        llave=[]
        dic=[]
        #Iniciamos la interfaz gráfica 
        app = QApplication(sys.argv)
        myWin = GUI_Main()
        
        #Obtenemos todas las llaves que vengan con el json
        for key in json_obj.keys():
            llave.append(key)
        
        #Usaremos un if que según que llave tenga se obtendrá la información 
        #del json y se mandara a la función interfaz.py
        if llave[0] == "vigilancia":
            dic =   json_obj.get('vigilancia')
            camaras(dic)
        elif llave[0] == "puertas":
            dic =   json_obj.get("puertas") 
            manejoPuertas(dic, myWin)
        elif llave[0] == "iluminacion":
            dic = json_obj.get("iluminacion")
            turnedOn(dic, myWin)
        elif llave[0] == "lucesGradual":
            dic = json_obj.get("lucesGradual")
            turned(dic, myWin)
        elif llave[0] == "timbre":
            dic = json_obj.get("timbre")
            son = detecciontimbre(dic, myWin)
            sonido(son)
        else:
            print("No se encontro valor")
        
        #Despliega la ventana
        myWin.show()
        sys.exit(app.exec_())
            

    """do_GET controla todas las solicitudes recibidas vía GET, es
    decir, páginas. Por seguridad, no se analizan variables que lleguen
    por esta vía"""
    def do_GET(self):
        # Revisamos si se accede a la raiz.
        # En ese caso se responde con la interfaz por defecto
        if self.path == '/':
            # 200 es el código de respuesta satisfactorio (OK)
            # de una solicitud
            self.send_response(200)
            # La cabecera HTTP siempre debe contener el tipo de datos mime
            # del contenido con el que responde el servidor
            self.send_header("Content-type", "text/html")
            # Fin de cabecera
            self.end_headers()
            # Por simplicidad, se devuelve como respuesta el contenido del
            # archivo html con el código de la página de interfaz de usuario
            self._serve_ui_file()
        # En caso contrario, se verifica que el archivo exista y se sirve
        else:
            self._serve_file(self.path[1:])

    """do_POST controla todas las solicitudes recibidas vía POST, es
    decir, envíos de formulario. Aquí se gestionan los comandos para
    la Raspberry Pi"""
    def do_POST(self):
        # Primero se obtiene la longitud de la cadena de datos recibida
        content_length = int(self.headers.get('Content-Length'))
        if content_length < 1:
            return
        # Después se lee toda la cadena de datos
        post_data = self.rfile.read(content_length)
        # Finalmente, se decodifica el objeto JSON y se procesan los datos.
        # Se descartan cadenas de datos mal formados
        try:
            jobj = json.loads(post_data.decode("utf-8"))
            self._parse_post(jobj)
        except:
            print(sys.exc_info())
            print("Datos POST no recnocidos")
            
def main():
    # Inicializa una nueva instancia de HTTPServer con el
    # HTTPRequestHandler definido en este archivo
    webServer = HTTPServer((address, port), WebServer)
    print("Servidor iniciado")
    print ("\tAtendiendo solicitudes en http://{}:{}".format(
        address, port))
    try:
        # Mantiene al servidor web ejecutándose en segundo plano
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Maneja la interrupción de cierre CTRL+C
        pass
    except:
        print(sys.exc_info())
    # Detiene el servidor web cerrando todas las conexiones
    webServer.server_close()
    # Reporta parada del servidor web en consola
    print("Server stopped.")


# Punto de anclaje de la función main
if __name__ == "__main__":
    main()
