#Algorithm
#1. Capture and store the background frame.  This will be done for some seconds 
#2. Detect the red colored cloth using color detection and segmentation algorithm.
#3. Segment out the red colored cloth by generating a mask. [ used in code ]
#4. Generate the final augmented output to create a magical effect. [ video.mp4 ]

#Color detection is a technique where we can detect any color in a given range of HSV color space.

#Image segmentation is the process of labeling every pixel in an image, where each pixel having the same label shares certain characteristics.

#HSV stands for HUE, SATURATION, and VALUE (or brightness). It is a cylindrical color space.

#HUE: The hues are modeled as an angular dimension which encodes color information.
#SATURATION: Saturation encodes intensity of color.
#VALUE: Value represents the brightness of the color.

#import packages
import cv2
import time
import numpy as np

#To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#initialize the camera
cap=cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for 2 seconds
#2-second delay between two captures are for adjusting camera auto exposure
time.sleep(2)
bg=0

#Capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()
#Flipping the background
bg = np.flip(bg, axis=1)

#Reading the captured frame until the camera is open
while (cap.isOpened()): #cap.isOpened() function checks if the camera is open or not and returns true if the camera is open and false if the camera is not open
    ret, img = cap.read()
    if not ret:
        break
    #Flipping the image for consistency
    img = np.flip(img, axis=1)

     #Converting the color from BGR to HSV
     #cv2.cvtColor() function converts colorspace.
     #OpenCV reads the frame as BGR colorspace. To detect any color first we have to convert the frame to HSV colorspace.
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #Generating mask to detect red colour
    #These values can also be changed as per the color
    #Lower bound and Upper bound are the boundaries of red color
    #cv2.inRange() function returns a segmented binary mask of the frame where the red color is present
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255,255])
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2

    #Open and expand the image where there is mask 1 (color)
    #morphologyEx(src, dst, op, kernel)
    #cv2.MORPH_OPEN removes unnecessary white noise from the black region. 
    #np.ones((3,3),np.uint8) create a 3×3 8 bit integer matrix.
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) 
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8)) #cv2.dilate increases white region in the image.

     #Selecting only the part that does not have mask one and saving in mask 2
     #cv2.bitwise_not() inverse the mask pixel value. Where the mask is white it returns black and where is black it returns white.
    mask_2 = cv2.bitwise_not(mask_1)

    #Keeping only the part of the images without the red color 
    #(or any other color you may choose)
    #cv2.bitwise_and() applies mask on frame in the region where mask is true (means white).
    res_1 = cv2.bitwise_and(img, img, mask=mask_2)

    #Keeping only the part of the images with the red color
    #(or any other color you may choose)
    res_2 = cv2.bitwise_and(bg, bg, mask=mask_1)

    #Generating the final output by merging res_1 and res_2
    finaloutput=cv2.addWeighted(res_1,1,res_2,1,0)
    output_file.write(finaloutput)
    #Displaying the output to the user
    cv2.imshow("magic",finaloutput)
    cv2.waitKey(1)



cap.release()
#out.release()
cv2.destroyAllWindows()