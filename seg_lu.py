import cv2
import numpy as np

video_path = "IMG_2721.mov"
capt = cv2.VideoCapture(video_path)

if not capt.isOpened():
    print("No se encuentra el archivo o el codec no es compatible.")
    exit()

bloques = [
    (586, 694, "Oscuridad a luz"),
    (1275, 1599, "Luz a oscuridad")
]

bloque = 0
frame = 0

capt.set(cv2.CAP_PROP_POS_FRAMES, bloques[bloque][0])
current_frame = bloques[bloque][0]

while bloque < len(bloques):
    inicio, final, nombre_ventana = bloques[bloque]

    ret, frame = capt.read()
    if not ret:
        break  #fin del video
    
    if inicio <= current_frame <= final: #si el frame actual está dentro del bloque de interés, lo procesamos
       
        crop = frame[180:420,330:600]
        gris = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        filtro = cv2.medianBlur(gris, 5)
        umbral, segmentada = cv2.threshold(filtro,0,255,cv2.THRESH_BINARY +cv2.THRESH_OTSU)
        cv2.imshow(nombre_ventana, segmentada)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): #Para salir presionar 'q'
            break
            
        frame += 1
    
    elif frame > final: #se salta al siguiente bloque
        bloque += 1
        if bloque < len(bloques):
            nuevo_inicio = bloques[bloque][0]
            capt.set(cv2.CAP_PROP_POS_FRAMES, nuevo_inicio)
            frame = nuevo_inicio
            cv2.destroyWindow(nombre_ventana) #se cierra la ventana anterior

capt.release()
cv2.destroyAllWindows()


#machetito para el futuro
#b, g, r = cv2.split(frame)
#textura_analizar = r