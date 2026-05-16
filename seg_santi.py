import cv2
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(BASE_DIR, "IMG_2721.mov")
capt = cv2.VideoCapture(video_path)

if not capt.isOpened():
    print("No se encuentra el archivo o el codec no es compatible.")
    exit()

bloques = [
    (586, 694, "Oscuridad a luz"),
    (1275, 1599, "Luz a oscuridad")
]

bloque = 0
capt.set(cv2.CAP_PROP_POS_FRAMES, bloques[bloque][0])
current_frame = bloques[bloque][0]

areas_pupila = []

while bloque < len(bloques):
    inicio, final, nombre_ventana = bloques[bloque]

    ret, img = capt.read()
    if not ret:
        break

    if inicio <= current_frame <= final:

        crop = img[180:420, 330:600]
        gris = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        filtro = cv2.medianBlur(gris, 7)

        # Hough circular para detectar la pupila
        circles = cv2.HoughCircles(
            filtro,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=50,
            param1=50,
            param2=30,
            minRadius=15,
            maxRadius=70
        )

        mascara_pupila = np.zeros_like(filtro)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            # Elegir el círculo más oscuro (la pupila)
            mejor = None
            min_brillo = 255
            for c in circles[0]:
                x, y, r = c
                mask_temp = np.zeros_like(filtro)
                cv2.circle(mask_temp, (x, y), r, 255, -1)
                brillo = cv2.mean(filtro, mask=mask_temp)[0]
                if brillo < min_brillo:
                    min_brillo = brillo
                    mejor = c

            if mejor is not None:
                x, y, r = mejor

                # Solo filtrar outliers extremos por rango de radio
                if 37 <= r <= 50:  # ajustar según lo que vea en video el radio 
                    area = np.pi * r**2
                    areas_pupila.append((current_frame, area, r))
                    cv2.circle(mascara_pupila, (x, y), r, 255, -1)
                    frame_vis = crop.copy()
                    cv2.circle(frame_vis, (x, y), r, (0, 255, 0), 2)
                    cv2.imshow("deteccion", frame_vis)
                    print(f"Frame {current_frame} | radio: {r}px")
                else:
                    areas_pupila.append((current_frame, None, None))
                    print(f"Frame {current_frame} | radio: {r}px | DESCARTADO (fuera de rango)")
            else:
                areas_pupila.append((current_frame, None, None))
                print(f"Frame {current_frame} | no detectado")

        cv2.imshow(nombre_ventana, mascara_pupila)
        print(f"Frame {current_frame}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        current_frame += 1

    elif current_frame > final:
        bloque += 1
        if bloque < len(bloques):
            nuevo_inicio = bloques[bloque][0]
            capt.set(cv2.CAP_PROP_POS_FRAMES, nuevo_inicio)
            current_frame = nuevo_inicio
            cv2.destroyWindow(nombre_ventana)

capt.release()
cv2.destroyAllWindows()


#machetito para el futuro
#b, g, r = cv2.split(frame)
#textura_analizar = r