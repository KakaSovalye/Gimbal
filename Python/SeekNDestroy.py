import cv2
from serial import Serial


# Yarım kod, kişiyi yakalayıp lazer ize vuracak kod olacaktı.

tetik=0


def KutuCiz(img, cerceve):
    x,y,w,h = int(cerceve[0]), int(cerceve[1]), int(cerceve[2]), int(cerceve[3])
    cv2.rectangle(img, (x,y),((x+w),(y+h)),(255,0,255),3 , 1)
    cv2.putText(img, 'Takipte', (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    arduinoData = 'X{0:d}Y{1:d}T{2:d}'.format((x + w // 2),
                                              (y + h // 2), tetik)
    print(arduinoData)
    ArduinoSerial.write(arduinoData.encode('utf-8'))

ArduinoSerial=Serial('com3',9600,timeout=0.1)

cap = cv2.VideoCapture(0)



takipci = None
cerceve = None

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    if (takipci is not None and cerceve is not None):
        success, cerceve = takipci.update(img)
        if success:
            KutuCiz(img, cerceve)
        else:
            cv2.putText(img, 'Goremiyorum', (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Takip',img)

    if (cv2.waitKey(1)& 0xff ==ord('q')):
        break
    elif (cv2.waitKey(1)& 0xff ==ord('f')):
        if tetik==0:
            tetik=1
        else:
            tetik=0
    elif (cv2.waitKey(1)&0xff == ord('t')):
        # takipci = cv2.TrackerMOSSE_create()
        takipci = cv2.TrackerCSRT_create()
        success, nimg = cap.read()
        nimg = cv2.flip(nimg,1)
        cv2.putText(nimg, 'Hedef Sec', (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cerceve = cv2.selectROI('Takip', nimg, False)
        takipci.init(img, cerceve)


