#Deep pi

##import nessesary libraries
from scipy.spatial import distance
import imutils
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import argparse #for test
import time
import dlib
import cv2
from playsound import playsound
import serial


# calculate eye aspect ratio (EAR)
def EAR_Calculater(point):
    p14 = distance.euclidean(point[0], point[3])
    p32 = distance.euclidean(point[1], point[5])
    p65 = distance.euclidean(point[2], point[4])
    Ear = (p65 + p32) / (p14 + p14)
    return Ear
    
#Create alarm using thread
def create_alarm():
    global alarm_status
    while alarm_status:
       playsound("1.mp3")

#countdown and send msg to arduino
def countdown():
    global  alarm_status
    global my_timer
    my_timer=5*60
    while alarm_status :
         mins, secs = divmod(my_timer, 60)
         timer = '{:02d}:{:02d}'.format(mins, secs)
         time.sleep(1)
         my_timer -= 1

         if(my_timer==0):
             msg =serial.Serial("dev/rfcomm1", baudrate=9600)
             msg.write(str(10))
             
#detect shape position
def Shape_Position(shape):
    (Leye_first, Leye_last) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]   # left_eye  = (42, 48))
    (Reye_first, Reye_last) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]  # right_eye = (36, 42)

    leftEye = shape[Leye_first:Leye_last]
    rightEye = shape[Reye_first:Reye_last]
    leftEAR = EAR_Calculater(leftEye)
    rightEAR = EAR_Calculater(rightEye)

    Avg_ear = (leftEAR + rightEAR) / 2.0
    return (Avg_ear, leftEye, rightEye)



#create parameters
EAR_Threshold = 0.25
NO_EAR_FRAMES = 22  #number of frame to make affect
alarm_status = False
count = 0
my_timer=60*5


#load models
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  #for detect faces
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  #for detect shap of eyes

###############################################
V_Stream= VideoStream(usePiCamera=True).start() 
time.sleep(1.0)

while True:
    frame = V_Stream.read()
    frame = imutils.resize(frame, width=777,height=777)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rect = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)

      for (x, y, w, h) in rect:
        rect = dlib.rectangle(int(x), int(y), int(x + w),int(y + h))
        cv2.rectangle(frame,(x,y),(x+w,y+h),(110,255,0),5,1 )

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        eye = Shape_Position(shape)
        Ear = eye[0]
        leftEye = eye [1]
        rightEye = eye[2]


        Leye = cv2.convexHull(leftEye)
        Reye = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [Leye,Reye], -1, (255, 255, 255), 2)
        if Ear < EAR_Threshold:
            count += 1
            if count >= NO_EAR_FRAMES:
                if alarm_status == False:
                    alarm_status = True
                    t = Thread(target=create_alarm)
                    t1 = Thread(target=countdown)
                    t.deamon = True
                    t.start()
                    t1.start()
                mi, se = divmod(my_timer, 60)
                help_timer = '{:02d}:{:02d}'.format(mi, se)
                cv2.putText(frame, "Call help in "+str(help_timer), (10, 90),
                            cv2.FONT_ITALIC, 0.7, (13, 212, 255), 2)
                cv2.putText(frame, "Sleep Alert", (10, 30),
                            cv2.FONT_ITALIC, 0.8, (255, 0, 255), 2)
        else:
            alarm_status = False
            count = 0

        cv2.putText(frame, "EAR: {:.2f}".format(Ear), (10, 60),
                    cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)

    cv2.imshow("Deep PI", frame)
     
     
     
    if (cv2.waitKey(1)& 0xFF== ord("q")): #change q to button read from driver
        break
cv2.destroyAllWindows()
V_Stream.stop()