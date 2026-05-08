import cv2

# Ruta al video .mov
video_path = 'IMG_2721.mov'

frame_deseado= 900 # frame que quiero ver

# Cargar el video
cap = cv2.VideoCapture(video_path)

#salto directo al frame que busco
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_deseado)
#Muestra la cantidad total de frames del video (1680)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(total_frames)
# Leer frame q quiero

#desde el 586 hasta el 694 oscuridad a luz
#desde 1275 hasta 1599 luz a oscuridad


ret, frame = cap.read()

if ret:
    cv2.imshow (f"mostrando el frame {frame_deseado}", frame)
    print("tocar tecla para terminar ventana")
    print(f"mostrando frame:{frame_deseado}")
    cv2.waitKey(0); #espera a que se presione una tecla
else:
    print ("no se pudio loko")

# Liberar recursos
cap.release()
cv2.destroyAllWindows()