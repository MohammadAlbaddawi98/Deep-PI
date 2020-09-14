#Deep pi

##import nessesary libraries
from scipy.spatial import distance
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import argparse
import imutils
import time
import dlib
import cv2
import os


# calculate eye aspect ratio (EAR)
def EAR_Calculater(point):
    p14 = distance.euclidean(point[0], point[3])
    p32 = distance.euclidean(point[1], point[5])
    p65 = distance.euclidean(point[2], point[4])
    Ear = (p65 + p32) / (p14 + p14)
    return Ear
    
#Create alarm using thread
def create_alarm(alarm):
    global alarm_status
    while alarm_status:
        s = 'espeak "'+alarm+'"'
        os.system(s)

#create parameters
EAR_THRESH = 0.3        
NO_EAR_FRAMES = 25  #number of frame to make affect
alarm_status = False
COUNTER = 0


#load models
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  #for detect faces
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  #for detect shap of eyes

###############################################
V_Stream= VideoStream(usePiCamera=True).start() 

while True:
    frame = V_Stream.read()

     
     
     
     
    if (cv2.waitKey(1)& 0xFF== ord("q")):
        break
cv2.destroyAllWindows()
V_Stream.stop()