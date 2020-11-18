import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
frame = cv2.resize(frame, (640,480))
filename = "photo.jpg"
cv2.imwrite(filename, frame)

cap.release()
cv2.destroyAllWindows()
