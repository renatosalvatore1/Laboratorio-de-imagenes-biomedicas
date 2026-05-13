import cv2
import numpy as np

video_path = "C:/Users/valle/Documents/Laboratorio-de-imagenes-biomedicas/IMG_2721.mov"
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
            
            #'''acá empieza k-means

            pixel_values = filtro.reshape((-1, 1))
            pixel_values = np.float32(pixel_values)

            criterios = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0) #Se detiene si se alcanza la precisión (0.2) o 10 iteraciones
            K = 4

            _, etiquetas, centros = cv2.kmeans(pixel_values, K, None, criterios, 10, cv2.KMEANS_RANDOM_CENTERS)
            centros = np.uint8(centros)
            segmentada_datos = centros[etiquetas.flatten()]
            segmentada = segmentada_datos.reshape((filtro.shape))
            cv2.imshow(nombre_ventana, segmentada)

            #acá termina k-means'''
            
            #cv2.imshow(nombre_ventana, filtro) #esto es para ver solo las filtradas
            
            if cv2.waitKey(30) & 0xFF == ord('q'): #waitKey de 30ms
                return True

desde_oscuro=bloques(586,695,capt,"Oscuridad a luz")
desde_luz=bloques(1275,1600,capt,"Luz a oscuridad")
capt.release()
cv2.destroyAllWindows()




#machetito para el futuro
#b, g, r = cv2.split(frame)
#textura_analizar = r