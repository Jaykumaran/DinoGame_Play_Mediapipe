import cv2
from cvzone.HandTrackingModule import HandDetector
from keyControl import PressKey,ReleaseKey,space_pressed
import time


detector = HandDetector(detectionCon=0.75,maxHands=1)
space_key_pressed = space_pressed
time.sleep(2)
current_key_pressed = set()  #gives non duplicate value when key pressed as set
cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    keyPressed = False
    space_pressed = False
    key_count =0
    key_pressed=0
    hands, img = detector.findHands(frame)
    cv2.rectangle(img,(0,480),(400,425),(255,255,255),-2)

    if hands:
        lmList = hands[0]
        fingerUp = detector.fingersUp(lmList)
        # print(fingerUp)
        if fingerUp == [0, 0, 0, 0, 0]:
            cv2.putText(frame, 'Dino Position: Jumping', (25, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4,
                        cv2.LINE_AA)
            if not space_pressed:
                PressKey(space_key_pressed)
                space_pressed = True
                current_key_pressed.add(space_key_pressed)
                key_pressed = space_key_pressed
                keyPressed = True
                key_count = key_count + 1
        else:
            space_pressed = False
            
        if fingerUp==[1,1,1,1,1]:
            cv2.putText(frame, 'Dino Position: Running', (25, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4,
                        cv2.LINE_AA)
        if not keyPressed and len(current_key_pressed) !=0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()  #making null after releasing
        elif key_count ==1 and len(current_key_pressed) ==2:  #qavoiding duplicates
            for key in current_key_pressed:
                if key_pressed!=key:
                    ReleaseKey(key)
            current_key_pressed = set()
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()

    cv2.imshow('Frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()