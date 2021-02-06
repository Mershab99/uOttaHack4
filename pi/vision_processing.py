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

# ROI settings
walkzone_start = (275,310)
walkzone_end = (460,460)
# settings for cropping
walkzone_start_x = 275
walkzone_end_x = 460
walkzone_start_y = 310
walkzone_end_y = 460
# Blue color in BGR 
color = (255, 0, 0) 
thickness = 4

previoustime = time.time() * 1000
# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    # performance indicator
    frametimer = time.time() *1000
    # Grab the raw NumPy array representing the image
    image = frame.array
    # walkzone ROI
    walkzoneROI = image[walkzone_start_y:walkzone_end_y,walkzone_start_x:walkzone_end_x]
    # Noise reduction
    blurredframe = cv2.blur(walkzoneROI, (3,3))
    # Subtraction
    fgmask = fgbg.apply(blurredframe)
    kernel = np.ones((5,5),np.uint16)
    # Noise reduction
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('frame',fgmask)
    n_black_pixels = np.sum(fgmask == 0)
    #print('number black pixel', n_black_pixels)
    # check if number of white pixels exceeds threshold of 5%
    # also check is cooldown time has passed, 500 millis current cooldown
    if(n_black_pixels < 27750*.95 and (time.time()*1000) - previoustime >500):
        print('movement detected!', n_black_pixels, 'time:', time.time())
        previoustime = time.time() * 1000
        filename = "{timestamp}.jpg".format(timestamp = time.time())
        #cv2.imwrite(filename, image)
    # Display the frame using OpenCV
    image = cv2.rectangle(image, walkzone_start, walkzone_end, color, thickness)
    cv2.imshow("Frame", image)
   
    cv2.imshow("cropped", walkzoneROI)
    # Wait for keyPress for 1 millisecond
    key = cv2.waitKey(1) & 0xFF
     
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
    elapsedtime = (time.time()*1000) - frametimer
    print("frame/millis", elapsedtime)
    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
