#Deep pi


##import nessesary libraries
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import os
############################################
# calculate eye aspect ratio (EAR)
def EAR(eye):
    p14 = dist.euclidean(eye[0], eye[3])
    p32 = dist.euclidean(eye[1], eye[5])
    p65 = dist.euclidean(eye[2], eye[4])
    Ear = (p65 + p32) / (p14 + p14)
    return Ear
#############################################
#load models
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  #for detect faces
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  #for detect shap of eyes

#############################################