import cv2

#this function 
ip=""
url=""
mensaje=[]

def lecturaIp():
    with open("ip.txt") as archivo:
        for linea in archivo:
            mensaje.append(linea)
    return mensaje

def escrituraIp(ip):
    f = open ('ip.txt','w')
    f.write(ip)
    f.close()
    
def escrituraLnsIp(msj):
    f = open("ip.txt", "w")
    f.writelines(msj)
    f.close()

def actualizacionIp(ip):
    f = open('ip.txt','a')
    f.write('\n' + ip)
    f.close()

def saveIp ():
    ip = str(input("Ingrese la ip a usar:"))
    url = "http:/"+ip+":8080/video"
    return url

    
mensaje = lecturaIp()

if len(mensaje) == 0:
    url = saveIp()
    escrituraIp(url)
else: 
    i=0
    while(i < len(mensaje)):
        print("[" + str(i+1) + "]" + " " + mensaje[i])
        i = i+1
    
    respuesta=str(input("Si desea elegir una IP ingrese su numero, si desea eliminar alguna ingrese e y si desea agregar ingrese a: "))
    
    if respuesta == 'e':
        res = int(input("Ingrese el numero a eliminar: "))
        try:
            mensaje.pop(res-1)
            escrituraLnsIp(mensaje)
        except Exception:
            print("No se puede eliminar la ip, posiblemente no existe, compruebe")
    elif respuesta == 'a':
        url = saveIp()
        actualizacionIp(url)
    else:
        try:
            url = mensaje[(int(respuesta)-1)]
        except:
            print("No existe la ip")

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