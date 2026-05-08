import cv2

cap = cv2.VideoCapture("IMG_2721.MOV")
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
