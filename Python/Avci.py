from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
from serial import Serial


#
# Encodins'de tanımlı kişlerden belirlenen kişiyi gördüğünde gimball kameranın takip etmesini sağlar
#

mevcutIsim = "bilinmiyor"
encodingsP = "encodings.pickle"
cascade = "Kaynaklar/haarcascades/haarcascade_frontalface_default.xml"

ArduinoSerial=Serial('com3',9600,timeout=0.1)

ArdX,ArdY,ArdT=0,0,0

eKam, bKam= 640,480

kamera=cv2.VideoCapture(0)
kamera.set(3, eKam)
kamera.set(4, bKam)

x,y=0,0

data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)

while True:
    basari, imaj = kamera.read()
    imaj = cv2.flip(imaj, 1)

    # 1280x768 için hedef
    # cv2.rectangle(imaj, (eKam // 2 - 100, bKam // 2 + 40),
    #               (eKam // 2 - 80, bKam // 2 + 70),
    #               (255, 255, 255), 3)


    # cv2.circle(imaj,(eKam // 2 - 70, bKam // 2 + 30),1,(255,255,0) ,4)
    #
    # cv2.circle(imaj, (eKam // 2 - 50, bKam // 2 + 50),1,(255,0,255) ,4)

    # 640x480 için hedef
    cv2.rectangle(imaj, (eKam // 2 - 70, bKam // 2 + 30),
                  (eKam // 2 - 50, bKam // 2 + 50),
                  (255, 255, 255), 3)
    x=(eKam // 2 - 70) - int(((eKam // 2 - 70)-(eKam // 2 - 50))/2)
    y=bKam // 2 + 30-int(((bKam // 2 + 30)-(bKam // 2 + 50))/2)

    # print(x,y)

    # print((eKam // 2 - 70, bKam // 2 + 30))
    # print((eKam // 2 - 50, bKam // 2 + 50))

    # cv2.circle(imaj,
    #            (640,10),
    #            1,
    #            (255, 0, 255),
    #            4)

    gri=cv2.cvtColor(imaj,cv2.COLOR_BGR2GRAY)

    cerceveler = detector.detectMultiScale(gri, scaleFactor=1.1,
                                      minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)

    kutular = [(y, x + w, y + h, x) for (x, y, w, h) in cerceveler]

    tanimlananlar = face_recognition.face_encodings(imaj, kutular)
    isimler = []

    for tanimli in tanimlananlar:
        esYuz = face_recognition.compare_faces(data["encodings"],
                                                 tanimli)

        isim = "Unknown"

        if True in esYuz:
            esYuzIdeks = [i for (i, b) in enumerate(esYuz) if b]
            adet = {}

            for i in esYuzIdeks:
                isim = data["names"][i]
                adet[isim] = adet.get(isim, 0) + 1

                isim = max(adet, key=adet.get)

            if mevcutIsim != isim:
                mevcutIsim = isim
                print(mevcutIsim)

        isimler.append(isim)

    for ((top, right, bottom, left), name) in zip(kutular, isimler):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(imaj, (left, top), (right, bottom),
                      (0, 255, 225), 2)

        # print(left,top,right,bottom)

        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(imaj, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    .8, (0, 255, 255), 2)
        if (name=='Berkin'):
            # print(left,top,right,bottom)
            # print('-------X--------')
            # print('Kare Merkez X')
            # print((left+int((left-right)/2)))
            # print('Lazer merkez X')
            # print(x)
            # print('Fark X')
            # print((left+int((abs(left-right))/2)-x))

            tarx=left+int(abs(left-right))
            tary=top-int(abs(bottom-top))

            if (tarx>x):
                ArdX=1
            elif (tarx<x):
                ArdX=-1
            else: Ardx=0
            # print('-------Y---------')
            # print('Kare Merkez Y')
            # print((top + int((abs(top - bottom)) / 2)))
            # print('Lazer merkez Y')
            # print(y)
            # print('Fark Y')
            # print((top + int((abs(top - bottom)) / 2) - y))

            if (tary>y):
                ArdY =1
            elif (tary<y):
                ArdY = -1
            else:
                ArdY = 0

            print(tarx,tary)
            print(x, y)


            arduinoData = 'X{0:d}Y{1:d}T{2:d}'.format(ArdX,
                                                ArdY,0)
            ArduinoSerial.write(arduinoData.encode('utf-8'))

            print(arduinoData)




    cv2.imshow('Goruntu', imaj)



    if cv2.waitKey(10)&0xFF== ord('q'):
        break