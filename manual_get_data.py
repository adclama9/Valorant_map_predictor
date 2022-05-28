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

    mask= cv2.imread('bw.png')

    while True: 

        print('new loop')
        if keyboard.read_key() == "p":
            time.sleep(1)
            continue
            
        elif keyboard.read_key() == "g":
            print("green win, saving...")
            write_all_images(images , 'g')
            images = []
            time.sleep(10)
            
        elif keyboard.read_key() == "r":
            print("red win, saving...")
            write_all_images(images , 'r')
            images = []
            time.sleep(10) 

        elif keyboard.read_key() == "e" :
            print("capturing map")
            map_capture = np.array(ImageGrab.grab(bbox=(86,77,535,549)))
            masked_image = cv2.bitwise_and(cv2.cvtColor(map_capture,cv2.COLOR_BGR2RGB), mask)
            print("Storing image")
            #accumulate images
            images.append(masked_image)
            time.sleep(1)
        elif keyboard.read_key() == "q" :
            sys.exit()
if __name__ == "__main__":
    main()
    
    
#https://www.vlr.gg/event/matches/926/valorant-champions-tour-stage-1-masters-reykjav-k/?series_id=all
#up to kru vs liquid    