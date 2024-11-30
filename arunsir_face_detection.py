import cv2
face_cascade = cv2.CascadeClassifier("/home/pi/face_detection/haarcascade_frontalface_default.xml")

cam = cv2.VideoCapture(0)

while True:
    _,img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray,1.1,4)
    
    for(x,y,w,h) in face:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
    cv2.imshow("image",img)
    k = cv2.waitKey(30) & 0xff
    if k ==27:
        break
    
cam.release()
cv2.destroyAllWindows()