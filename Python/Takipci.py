
import cv2
import time
from serial import Serial
import mediapipe as mp


#
# Gimball kamera bir yüz gördüğünde o yüzü takip eder
#

eKam, bKam= 640,480

yakala=cv2.VideoCapture(0)
yakala.set(3,eKam)
yakala.set(4,bKam)

tetik=0

ArduinoSerial=Serial('com3',9600,timeout=0.1)

mpYuzYakala = mp.solutions.face_detection
mpCiz = mp.solutions.drawing_utils
yuzYakalama = mpYuzYakala.FaceDetection(0.7)


while True:
    basarili, imaj= yakala.read()
    imaj=cv2.flip(imaj,1)  #aynalama

    ih, iw, ic = imaj.shape

    # cv2.rectangle(imaj, (eKam // 2 - 70, bKam // 2 + 30),
    #               (eKam // 2 - 50, bKam // 2 + 50),
    #               (255, 255, 255), 3)

    imajRGB = cv2.cvtColor(imaj, cv2.COLOR_BGR2RGB)

    sonuclar = yuzYakalama.process(imajRGB)

    # cv2.rectangle(imaj, (640 // 2 - 30, 480 // 2 - 30),
    #               (640 // 2 + 30, 480 // 2 + 30),
    #               (255, 255, 255), 3)

    if sonuclar.detections:
        for id, yakalanan in enumerate(sonuclar.detections):
            # mpCiz.draw_detection(imaj,yakalanan)
            CehreCerceveC = yakalanan.location_data.relative_bounding_box
            CehreCerceve = int(CehreCerceveC.xmin * iw), int(CehreCerceveC.ymin * ih), \
                           int(CehreCerceveC.width * iw), int(CehreCerceveC.height * ih)

            cv2.rectangle(imaj, CehreCerceve, (255,0,255),2)
            # cv2.circle(imaj, (CehreCerceve[0] + CehreCerceve[2] // 2, CehreCerceve[1] + CehreCerceve[3] // 2), 2, (0, 255, 0), 2)


            arduinoData = 'X{0:d}Y{1:d}T{2:d}'.format((CehreCerceve[0]+CehreCerceve[2]//2),(CehreCerceve[1]+CehreCerceve[3]//2),tetik)
            print(arduinoData)
            ArduinoSerial.write(arduinoData.encode('utf-8'))



    cv2.imshow('Görüntü',imaj)

    '''test amaçlı
    read= str(ArduinoSerial.readline(ArduinoSerial.inWaiting()))
    time.sleep(0.05)
    print('data from arduino:'+read)
    '''

    if cv2.waitKey(10)&0xFF== ord('t'):
        if(tetik==1):
            tetik=0
        else: tetik=1

    if cv2.waitKey(10)&0xFF== ord('q'):
        break
