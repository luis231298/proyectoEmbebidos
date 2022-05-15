import cv2

#this function 
ip=""
url=""

def lecturaIp():
    pass

def saveIp ():
    ip = str(input("Ingrese la ip a usar:"))
    url = "http:/"+ip+":8080/video"
    return url
 
url = saveIp()
print(url)


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