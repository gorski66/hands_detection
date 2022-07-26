import cv2
import time
import os
import HandDetection as htm
import mediapipe as mp
wCam,hCam = 720, 640


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

folderPathL="FingerImagesL"
folderPathR="FingerImagesR"
folderPathLR="FingerImagesLR"
folderPathRR="FingerImagesRR"
myListL = os.listdir(folderPathL)
myListR = os.listdir(folderPathR)
myListLR = os.listdir(folderPathL)
myListRR = os.listdir(folderPathR)

overlayListL = []
overlayListR = []
overlayListLR = []
overlayListRR = []

for imPathL in myListL:
    image = cv2.imread(f'{folderPathL}/{imPathL}')
    overlayListL.append(image)

for imPathR in myListR:
    image = cv2.imread(f'{folderPathR}/{imPathR}')
    overlayListR.append(image)

for imPathLR in myListLR:
    image = cv2.imread(f'{folderPathLR}/{imPathLR}')
    overlayListLR.append(image)

for imPathRR in myListRR:
    image = cv2.imread(f'{folderPathRR}/{imPathRR}')
    overlayListRR.append(image)


pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]


while cap.isOpened():
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)


    #print(lmList)

    if len(lmList) != 0:
        fingers=[]
        handside = detector.check_hand()

        if handside[0] == "Left":

            rotate = 0

            if lmList[4][1] > lmList[20][1]:
                cv2.putText(img, f'right hand', (lmList[0][1], lmList[0][2]+20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
            else:
                cv2.putText(img, f'right hand rotated', (lmList[0][1], lmList[0][2] + 20), cv2.FONT_HERSHEY_PLAIN, 1,(255, 255, 255), 2)
                rotate = 1

            if rotate == 0:
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)


            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            #print(fingers)
            totalFingers = fingers.count(1)
            #print(totalFingers)

            if rotate == 0:
                h,w,c = overlayListR[0].shape
                img[0:h, 540:640] = overlayListR[totalFingers-1]
            else:
                h, w, c = overlayListRR[0].shape
                img[0:h, 540:640] = overlayListRR[totalFingers - 1]


        if handside[0] == "Right":
            rotate = 0
            if lmList[4][1] < lmList[20][1]:
                cv2.putText(img, f'left hand', (lmList[0][1], lmList[0][2] + 20), cv2.FONT_HERSHEY_PLAIN, 1,(255, 255, 255), 2)
            else:
                cv2.putText(img, f'left hand rotated', (lmList[0][1], lmList[0][2] + 20), cv2.FONT_HERSHEY_PLAIN, 1,(255, 255, 255), 2)
                rotate = 1

            if rotate == 0:

                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            else:

                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)


            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            #print(fingers)
            totalFingers = fingers.count(1)
            # print(totalFingers)
            if rotate == 0:
                h, w, c = overlayListL[0].shape
                img[0:h, 0:w] = overlayListL[totalFingers - 1]
            else:
                h, w, c = overlayListLR[0].shape
                img[0:h, 0:w] = overlayListLR[totalFingers - 1]






    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS:{int(fps)}',(260,30),cv2.FONT_HERSHEY_PLAIN,2,(173,255,47),3)

    cv2.imshow("Camera",img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
