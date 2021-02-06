from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np
# Initialize the camera
camera = PiCamera()
 
# Set the camera resolution
camera.resolution = (960, 720)
 
# Set the number of frames per second
camera.framerate = 32
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(960, 720))
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
fgbg = cv2.createBackgroundSubtractorMOG2(history = 8)
sanitizer_motion = cv2.createBackgroundSubtractorMOG2(history = 8)

# ROI settings
walkzone_start_x = (int)(275*1.5)
walkzone_end_x = (int)(460*1.5)
walkzone_start_y = (int)(310*1.5)
walkzone_end_y = (int)(460*1.5)
walkzone_start = (walkzone_start_x ,walkzone_start_y)
walkzone_end = (walkzone_end_x,walkzone_end_y)

sanitizer_start_x = (int)(55*1.5)
sanitizer_end_x = (int)(60*1.5)
sanitizer_start_y = (int)(385*1.5)
sanitizer_end_y = (int)(395*1.5)
sanitizer_start = (sanitizer_start_x, sanitizer_start_y)
sanitizer_end = (sanitizer_end_x, sanitizer_end_y)

# Blue color in BGR 
color = (255, 0, 0) 
thickness = 4

walk_in_state = False
entering = False
leaving = False

previoustime = time.time() * 1000
# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

    frametimer = time.time() *1000
    # Grab the raw NumPy array representing the image
    image = frame.array
    # walkzone ROI
    walkzoneROI = image[walkzone_start_y:walkzone_end_y,walkzone_start_x:walkzone_end_x]
    cv2.imshow("cropped", walkzoneROI)
    blurredframe = cv2.blur(walkzoneROI, (3,3)) 
    fgmask = fgbg.apply(blurredframe)
    kernel = np.ones((5,5),np.uint16)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('frame',fgmask)
    
    #walk-in or walk-out algorithm
    height = walkzoneROI.shape[0]
    width = walkzoneROI.shape[1]
    walkzoneROI = cv2.rectangle(walkzoneROI, (0,0), ((int)(width), (int)(height*.2)), color, thickness)
    walking_in_walkzone = fgmask[0:(int)(height*.2),0:(int)(width)]
    walking_out_walkzone = fgmask[(int)(height*.7): height,0:(int)(width)]
    walk_in_threshold = 0.85*(width * (height *.2))
    walk_out_threshold = 0.9*(width * (height *.3))
    walk_in_b_pixels = np.sum(walking_in_walkzone == 0)
    walk_out_b_pixels = np.sum(walking_out_walkzone == 0)
    # near 0 value 
    if(walk_in_b_pixels > 0.95*(width * (height *.2)) and walk_out_b_pixels > 0.95*(width * (height *.3))):
        walk_in_state = False
        leaving = False
        #print("false ------------------")
    if(not walk_in_state):
        
        if(walk_in_b_pixels < walk_in_threshold and  walk_out_b_pixels > walk_out_threshold):
            print(">>>>>>>>>>WALK IN DETECTED!>>>>>>>>>")
            walk_in_state = True
            entering = True
            leaving = False
            # debug
            # print("walk in threshold", walk_in_threshold)
            # print("walk out threshold", walk_out_threshold)
            # print("walk_in_b_pixels: ", walk_in_b_pixels)
            # print("walk_out_b_pixels: ", walk_out_b_pixels)
        elif(walk_out_b_pixels < 0.98*(width * (height *.3))):
            print("<<<<<<<<<<WALK OUT DETECTED!<<<<<<<<")
            walk_in_state = True
            entering = False
            leaving = True
            # debug
            # print("walk in threshold", walk_in_threshold)
            # print("walk out threshold", walk_out_threshold)
            # print("walk_in_b_pixels: ", walk_in_b_pixels)
            # print("walk_out_b_pixels: ", walk_out_b_pixels)
    cv2.imshow("walk out zone", walking_out_walkzone)
    cv2.imshow("walk in zone", walking_in_walkzone)
    
    #Movement detection
    n_black_pixels = np.sum(fgmask == 0)
    #print('number black pixel', n_black_pixels)
    # check if number of white pixels exceeds threshold of 5%
    # also check is cooldown time has passed, 500 millis current cooldown
    pixel_threshold = (walkzone_end_y-walkzone_start_y)*(walkzone_end_x-walkzone_start_x)
    if(n_black_pixels < pixel_threshold*.95 and (time.time()*1000) - previoustime >150):
        print('movement detected!', n_black_pixels, 'time:', time.time())
        if(leaving):
            filename = "leaving_{timestamp}.jpg".format(timestamp = time.time())
        else:
            filename = "entering_{timestamp}.jpg".format(timestamp = time.time())
        previoustime = time.time() * 1000
        
        #cv2.imwrite(filename, image)
    # Display the frame using OpenCV
    image = cv2.rectangle(image, walkzone_start, walkzone_end, color, thickness)
    
    
    # Hand sanitizer detection
    image = cv2.rectangle(image, sanitizer_start, sanitizer_end, color, thickness)
    
    sanitizerROI = image[sanitizer_start_y: sanitizer_end_y, sanitizer_start_x: sanitizer_end_x]
    sanitizerROI = cv2.blur(sanitizerROI, (3,3))
    sanitizer_movement = sanitizer_motion.apply(sanitizerROI)
    s_height = sanitizer_movement.shape[0]
    s_width = sanitizer_movement.shape[1]
    s_threshold = s_height*s_width*0.95
    if(np.sum(sanitizer_movement == 0) < s_threshold):
        print("==========THANKS FOR USING SANITIZER============")
    #cv2.imshow("sanitizer", sanitizer_movement)
    cv2.imshow("Frame", image)
    # Wait for keyPress for 1 millisecond
    key = cv2.waitKey(1) & 0xFF
     
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
    # performance timer
    elapsedtime = (time.time()*1000) - frametimer
    #print("frame/millis", elapsedtime)
    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
