import cv2
import time
from serial import Serial
import mediapipe as mp
import math

#
# Birinci kamerada gördüğü el hareketlerine göre Gimball kamerayı haraket ettirir
#

ArduinoSerial=Serial('com3',9600,timeout=0.1)

motordik, motoryat = 0, 0

eKam, bKam = 640, 480

robotGoz = cv2.VideoCapture(0)
yakala = cv2.VideoCapture(1)
yakala.set(3, eKam)
yakala.set(4, bKam)


def Mesafe(p1, p2):
    return float(math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)))






mpElYakala = mp.solutions.hands
mpCiz = mp.solutions.drawing_utils
eller = mpElYakala.Hands(False, 1, 0.75)

merkezData, tetikData = [], []
yHareket, xHareket, xTetik = False, False, False
xkontrol = 1

ArduinoAcik, lmGorunur= False, False

ArdX, ArdY, Tetik = 0, 0, 0
capa, orta, bas, merkez = [0, 0], [0, 0], [0, 0], [0, 0]

while True:
    basarili, imaj = yakala.read()
    basarili2, imaj2= robotGoz.read()

    cv2.line(imaj2,((eKam // 2 + 60, bKam // 2 + 12)),((eKam // 2 + 60, bKam // 2 + 30)),(0, 177, 64),2)
    cv2.line(imaj2, ((eKam // 2 + 60, bKam // 2 + 47)), ((eKam // 2 + 60, bKam // 2 + 62)), (0, 177, 64), 2)
    cv2.line(imaj2, ((eKam // 2 + 30, bKam // 2 + 40)), ((eKam // 2 + 40, bKam // 2 + 40)), (0, 177, 64), 2)
    cv2.line(imaj2, ((eKam // 2 + 80, bKam // 2 + 40)), ((eKam // 2 + 90, bKam // 2 + 40)), (0, 177, 64), 2)

    if (ArduinoAcik):
        cv2.circle(imaj,(620,10),4,(0,0,255),5)
    # cv2.rectangle(imaj2, (eKam // 2 + 70, bKam // 2 + 30),
    #               (eKam // 2 + 50, bKam // 2 + 50),
    #               (255, 255, 255), 3)

    imaj = cv2.flip(imaj, 1)  # aynalama
    imajRGB = cv2.cvtColor(imaj, cv2.COLOR_BGR2RGB)

    h, w, c = imaj.shape

    sonuclar = eller.process(imajRGB)
    capax, capay, ortax, ortay, basx, basy, xtetikx, tetiky = 0, 0, 0, 0, 0, 0, 0, 0

    if sonuclar.multi_hand_landmarks:
        for el in sonuclar.multi_hand_landmarks:
            for id, lm in enumerate(el.landmark):
                if (lmGorunur):
                    mpCiz.draw_landmarks(imaj,el,mpElYakala.HAND_CONNECTIONS)
                elpx, elpy = int(lm.x * w), int(lm.y * h)

                if (id == 9):  # çapa

                    capa = [lm.x, lm.y]

                    capax, capay = lm.x, lm.y

                    if (lmGorunur):
                        cv2.circle(imaj, (elpx, elpy), 5, (255, 255, 0), cv2.FILLED)

                if (id == 12):  # dikeyci

                    orta = [lm.x, lm.y]
                    ortax, ortay = lm.x, lm.y

                    if (lmGorunur):
                        cv2.circle(imaj, (elpx, elpy), 5, (255, 255, 0), cv2.FILLED)

                if (id == 4):  # tetik 20
                    bas = [lm.x, lm.y]
                    basx, basy = lm.x, lm.y

                    if (lmGorunur):
                        cv2.circle(imaj, (elpx, elpy), 5, (255, 255, 0), cv2.FILLED)

                if (id == 0):
                    merkez = [lm.x, lm.y]
                    merkezx, merkezy = lm.x, lm.y

            if (capax > ortax):
                motoryat = -1
            else:
                motoryat = 1
            # print(motoryat)

            if (capay > ortay):
                motordik = -1
            else:
                motordik = 1

            merkezData.append(Mesafe(merkez, capa))

            if (abs(ortax - capax) > Mesafe(merkez, capa) / 4):
                xHareket = True
            else:
                xHareket = False

            # print(xhareket)

            if (abs(ortay - capay) > Mesafe(merkez, capa) / 2):
                yHareket = True
            else:
                yHareket = False

            if (abs(basx - capax) < Mesafe(merkez, capa) / 4):
                xTetik = True
            else:
                xTetik = False

            # print(yhareket)

    if (len(tetikData) == 0):
        TetAv = 1
    else:
        TetAv = sum(tetikData) / len(tetikData)

    if (len(merkezData) == 0):
        MerkezAv = 0.000000001
    else:
        MerkezAv = sum(merkezData) / len(merkezData)

    if (motordik > 0 and yHareket):
        ArdY = 1
    elif (motordik < 0 and yHareket):

        ArdY = -1
    else:
        ArdY = 0


    # xkontrol bağlaman lazım
    if (motoryat > 0 and xHareket):
        ArdX = -1*xkontrol
    elif (motoryat < 0 and xHareket):
        ArdX = 1*xkontrol
    else:
        ArdX = 0

    if (ArdY == 0 and ArdX == 0):
        if (xTetik):
            Tetik = 1
        else:
            Tetik = 0
    else:
        Tetik = 0

    # print(Dik)
    # print(Yat)

    arduinoData = 'X{0:d}Y{1:d}T{2:d}'.format(ArdX, ArdY, Tetik)
    if (ArduinoAcik):
        ArduinoSerial.write(arduinoData.encode('utf-8'))
    # print(ArdX)
    # print(ArdY)
    # print(Tetik)

    print(arduinoData)



    merkezData, tetikData = [], []





    cv2.imshow("El Okuyucu", imaj)
    cv2.imshow("Robot Gozu2", imaj2)

    if cv2.waitKey(10) & 0xFF == ord('a'):
        if (xkontrol == 1):
            xkontrol = -1
        else:
            xkontrol = 1

    if cv2.waitKey(10) & 0xFF == ord('r'):
        if (ArduinoAcik == True):
            ArduinoAcik = False
        else:
            ArduinoAcik = True

    if cv2.waitKey(10) & 0xFF == ord('g'):
        if (lmGorunur==False):
            lmGorunur=True
        else: lmGorunur=False


    if cv2.waitKey(10) & 0xFF == ord('q'):
        break