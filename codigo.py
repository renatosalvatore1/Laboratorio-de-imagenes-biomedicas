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



cap = cv2.VideoCapture("video.MOV")
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

def on_trackbar(pos):
    cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
    ret, frame = cap.read()
    if ret:
        cv2.putText(frame, f"Frame: {pos}/{total_frames-1}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Video", frame)

cv2.namedWindow("Video")
cv2.createTrackbar("Frame", "Video", 0, total_frames - 1, on_trackbar)

# Mostrar el primer frame
on_trackbar(0)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()