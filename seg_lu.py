import cv2
import numpy as np

video_path = 'C:/Users/valle/Documents/Laboratorio-de-imagenes-biomedicas/IMG_2721.mov' 
capt = cv2.VideoCapture(video_path)

'''trabajo con bloques de frames (586,694) para oscuridad a luz y (1275,1599) para luz a oscuridad'''

def bloques(inicio, final, cap, nombre_ventana): 
    if not cap.isOpened():
        print("No se encuentra el archivo o el codec no es compatible.")
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, inicio)
        
        while True:
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            ret, frame = cap.read()
            
            if not ret or current_frame > final: #salimos si el video termina o se pasa del rango
                break
                
            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            filtro = cv2.medianBlur(gris, 5)
            
            cv2.imshow(nombre_ventana, filtro)
            
            print("Apretar q para finalizar")
            if cv2.waitKey(30) & 0xFF == ord('q'): #waitKey de 30ms
                return "Proceso interrumpido por el usuario."

desde_oscuro=bloques(586,695,capt,"Oscuridad a luz")
desde_luz=bloques(1275,1600,capt,"Luz a oscuridad")
capt.release()
cv2.destroyAllWindows()