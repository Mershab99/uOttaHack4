from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np
# Initialize the camera
camera = PiCamera()
 
# Set the camera resolution
camera.resolution = (640, 480)
 
# Set the number of frames per second
camera.framerate = 32
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(640, 480))
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
fgbg = cv2.createBackgroundSubtractorMOG2(history = 8)
previoustime = time.time() * 1000
# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    # Performace timer
    frametimer = time.time() *1000
    # Grab the raw NumPy array representing the image
    image = frame.array
    blurredframe = cv2.blur(image, (3,3)) 
    fgmask = fgbg.apply(blurredframe)
    kernel = np.ones((5,5),np.uint16)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('frame',fgmask)
    n_black_pixels = np.sum(fgmask == 0)
    #print('number black pixel', n_black_pixels)
    # check if number of white pixels exceeds threshold of 5%
    # also check is cooldown time has passed, 500 millis current cooldown
    if(n_black_pixels < 307200*.95 and (time.time()*1000) - previoustime >500):
        print('movement detected!', n_black_pixels, 'time:', time.time())
        # reset cooldown timer
        previoustime = time.time() * 1000
        # save image
        filename = "{timestamp}.jpg".format(timestamp = time.time())
        cv2.imwrite(filename, image)
    # Display the frame using OpenCV
    #cv2.imshow("Frame", image)
     
    # Wait for keyPress for 1 millisecond
    key = cv2.waitKey(1) & 0xFF
     
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
    # time it takes per frame
    elapsedtime = (time.time()*1000) - frametimer
    print("frame/millis", elapsedtime)
    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
