import numpy as np
from PIL import ImageGrab
import cv2
import time
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = 'C:/OCR/tesseract.exe'
from PIL import Image
from threading import Thread

def screen_record_map():
    # bbox (left, upper, right, lower)
    mask = cv2.imread('bw.png')
    mask = cv2.resize(mask, dsize=(336, 352), interpolation=cv2.INTER_CUBIC)
  
    while True:
    
        printscreen = np.array(ImageGrab.grab(bbox=(65,60,401,412)))
        cv2.imshow('window2',printscreen)
        masked_image = cv2.bitwise_and(cv2.cvtColor(printscreen,cv2.COLOR_BGR2RGB), mask)
        cv2.imshow('window1',masked_image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            

            
def screen_record_score_left():
    while True:
        left ,right = 1060,1170
        image = np.array(ImageGrab.grab(bbox=(left,0,right,90)))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # OCR
        left_num = pytesseract.image_to_string(thresh, lang='eng', config='--psm 10')
        cv2.imshow('window', thresh)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

            
def screen_record_score_right():
    while True:
        left ,right = 1400,1490
        image = np.array(ImageGrab.grab(bbox=(left,0,right,90)))
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # OCR
        right_num = pytesseract.image_to_string(thresh, lang='eng', config='--psm 10')
        #print(right_num)
        #print(right_num.isdigit())
        
        cv2.imshow('window', thresh)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
            
            
def test_shit():
    while True:
        left ,right = 1400,1490
        image = np.array(ImageGrab.grab(bbox=(left,0,right,90)))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        cv2.imshow('window', thresh)
        num = pytesseract.image_to_string(thresh, lang='eng', config='--psm 10')
        print(num)
        if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
                
            #print(right_num.isdigit())
        
        
       
def test_2():    
    for i in range(0,14):
        with open(str(i)+'.gt.txt','w') as f:
            f.write(str(i))
        
    pass

screen_record_map()
#test_2()

#if __name__== '__main__':
#    Thread(target = func1).start()
#    Thread(target = func2).start()

#screen_record_score_right()
#test_shit()