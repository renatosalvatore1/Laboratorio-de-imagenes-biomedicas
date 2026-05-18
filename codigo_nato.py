
from numpy.lib import introspect
from numpy.lib import introspect
import matplotlib.pyplot as plt
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
                if 37 <= r <= 50:
                    area = np.pi * r**2
                    areas_pupila.append((current_frame, area, r, int(x), int(y)))
                    cv2.circle(mascara_pupila, (x, y), r, 255, -1)
            else:
                areas_pupila.append((current_frame, None, None, None, None))

        current_frame += 1

    elif current_frame > final:
        bloque += 1
        if bloque < len(bloques):
            nuevo_inicio = bloques[bloque][0]
            capt.set(cv2.CAP_PROP_POS_FRAMES, nuevo_inicio)
            current_frame = nuevo_inicio

capt.release()
cv2.destroyAllWindows()


# --- Filtrado de outliers por IQR (radio + distancia al centro) ---

# Centro del crop: img[180:420, 330:600] → ancho=270, alto=240
CX_CROP, CY_CROP = 135, 120

# Extraer frames con detección válida
radios_validos = [
    (frame, r, x, y)
    for frame, area, r, x, y in areas_pupila
    if r is not None
]

if radios_validos:
    radios = np.array([r for _, r, _, _ in radios_validos], dtype=float)
    # Cast a int para evitar overflow con uint16
    distancias = np.array(
        [np.sqrt((x - CX_CROP)**2 + (y - CY_CROP)**2) for _, _, x, y in radios_validos],
        dtype=float
    )

    # IQR sobre radios
    Q1r, Q3r = np.percentile(radios, 25), np.percentile(radios, 75)
    IQRr = Q3r - Q1r
    lim_r_inf, lim_r_sup = Q1r - 1.5 * IQRr, Q3r + 1.5 * IQRr

    # IQR sobre distancia al centro (solo límite superior)
    Q3d = np.percentile(distancias, 75)
    IQRd = Q3d - np.percentile(distancias, 25)
    lim_d_sup = Q3d + 1.5 * IQRd

    datos_pupila = np.array(
        [[frame, r * 2] for frame, r, x, y in radios_validos
         if lim_r_inf <= r <= lim_r_sup
         and np.sqrt((x - CX_CROP)**2 + (y - CY_CROP)**2) <= lim_d_sup]
    )
else:
    datos_pupila = np.array([])

# --- Arrays por bloque usando la variable 'bloques' ---
if len(datos_pupila) > 0:
    inicio0, final0, _ = bloques[0]
    inicio1, final1, _ = bloques[1]

    oscuridad_luz = datos_pupila[
        (datos_pupila[:, 0] >= inicio0) & (datos_pupila[:, 0] <= final0), 1
    ]
    luz_oscuridad = datos_pupila[
        (datos_pupila[:, 0] >= inicio1) & (datos_pupila[:, 0] <= final1), 1
    ]
else:
    oscuridad_luz = np.array([])
    luz_oscuridad = np.array([])

print(oscuridad_luz)
print(luz_oscuridad)


t1 = np.arange(len(oscuridad_luz))
t2 = np.arange(len(luz_oscuridad))

# --- Métricas de la pupila ---
def calcular_metricas(arr, nombre):
    if len(arr) < 2:
        print(f"{nombre}: datos insuficientes")
        return
    diff = np.diff(arr.astype(float))  # cambio frame a frame
    contraccion_total = arr.max() - arr.min()
    vel_max_dilatacion  = diff.max()
    vel_max_contraccion = diff.min()

    diffs_pos = diff[diff > 0]  # solo aumentos
    diffs_neg = diff[diff < 0]  # solo caídas
    vel_media_dilatacion  = diffs_pos.mean() if len(diffs_pos) > 0 else 0
    vel_media_contraccion = diffs_neg.mean() if len(diffs_neg) > 0 else 0

    print(f"\n=== {nombre} ===")
    print(f"  Diámetro inicial : {arr[0]} px")
    print(f"  Diámetro final   : {arr[-1]} px")
    print(f"  Variación total  : {arr[-1] - arr[0]:+d} px  (min={arr.min()}, max={arr.max()})")
    print(f"  Contracción total (max-min): {contraccion_total} px")
    print(f"  Vel. máx. dilatación  : +{vel_max_dilatacion:.1f} px/frame")
    print(f"  Vel. máx. contracción : {vel_max_contraccion:.1f} px/frame")
    print(f"  Vel. media dilatación : +{vel_media_dilatacion:.2f} px/frame")
    print(f"  Vel. media contracción: {vel_media_contraccion:.2f} px/frame")


calcular_metricas(oscuridad_luz, "Oscuridad → Luz")
calcular_metricas(luz_oscuridad, "Luz → Oscuridad")


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

# --- Oscuridad a luz ---
ax1.plot(t1, oscuridad_luz, color="steelblue", alpha=0.7, label="Diámetro")
if len(t1) >= 2:
    coef1 = np.polyfit(t1, oscuridad_luz, 1)
    tendencia1 = np.poly1d(coef1)
    ax1.plot(t1, tendencia1(t1), color="red", linewidth=2, linestyle="--", label=f"Tendencia ({coef1[0]:+.2f} px/frame)")
ax1.set_title("Oscuridad → Luz")
ax1.set_xlabel("Frame (relativo)")
ax1.set_ylabel("Diámetro pupila (px)")
ax1.legend()
ax1.grid(True, alpha=0.3)

# --- Luz a oscuridad ---
ax2.plot(t2, luz_oscuridad, color="darkorange", alpha=0.7, label="Diámetro")
if len(t2) >= 2:
    coef2 = np.polyfit(t2, luz_oscuridad, 1)
    tendencia2 = np.poly1d(coef2)
    ax2.plot(t2, tendencia2(t2), color="red", linewidth=2, linestyle="--", label=f"Tendencia ({coef2[0]:+.2f} px/frame)")
ax2.set_title("Luz → Oscuridad")
ax2.set_xlabel("Frame (relativo)")
ax2.set_ylabel("Diámetro pupila (px)")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
#plt.savefig('grafico_pupila.png', dpi=300, bbox_inches='tight')
plt.show()