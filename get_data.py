import numpy as np
from PIL import ImageGrab
import cv2
import time
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = 'C:/OCR/tesseract.exe'
from PIL import Image
from threading import Thread
import sys
import keyboard
import os 

working_directory = os.getcwd()

def tryint(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False




# Green == left team, red == right team 
#OCR func to convert the image to a number
def get_num(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    num = pytesseract.image_to_string(thresh, lang='eng', config='--psm 10')
    return num

# color is g or r 

def write_all_images(list_of_images,color):
    if color == 'g':
        path = working_directory+"/train_images/green/"
    else:
        path = working_directory+"/train_images/red/"
    for image in list_of_images:
        cv2.imwrite(path+color+str(time.time())+'.png', image)
def main():   
    images = []    
    green_count = 0
    red_count = 0 
    red_bbox = (1400,0,1490,90)
    green_bbox = (1060,0,1170,90)
    mask= cv2.imread('bw.png')

    while True: 
        print("capturing numbers")
        #green num 
        green_num_capture = np.array(ImageGrab.grab(bbox=green_bbox))
        green_num = get_num(green_num_capture)
        
        red_num_capture = np.array(ImageGrab.grab(bbox=red_bbox))
        red_num = get_num(red_num_capture)
        print(green_num,red_num)
        
        if tryint(green_num) == False or tryint(red_num) == False:
            time.sleep(2)
            continue
        
        print("capturing map")
            
        map_capture = np.array(ImageGrab.grab(bbox=(86,77,535,549)))
        masked_image = cv2.bitwise_and(cv2.cvtColor(map_capture,cv2.COLOR_BGR2RGB), mask)
        
        green_num.strip('\n')
        red_num.strip('\n')
        green_num = int(green_num)
        red_num = int(red_num)
        
        
        if green_num == (green_count+1):
            #increment ,save as  left win
            print("green win, saving...")
            write_all_images(images , 'g')
            images = []
            green_count += 1
            time.sleep(10) #add sleep so that round over images not captured
            
        elif red_num == (red_count+1):
            #increment, save as right win, 
            print("red win, saving...")
            write_all_images(images , 'r')
            images = []
            red_count += 1
            time.sleep(10) 
            
        elif green_num == 13 or red_num == 13:
            print('End Game')
            sys.exit()
            
        else:
            print("Storing image")
            #accumulate images
            images.append(masked_image)
            time.sleep(1)
            
if __name__ == "__main__":
    main()

