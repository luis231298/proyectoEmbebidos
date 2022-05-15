import cv2

#this function 
ip=""
url=""

def saveIp ():
    ip = str(input("Ingrese la ip a usar:"))
    url = "http:/"+ip+":8080/video"
    return url
 
url=saveIp()
print(url)
    