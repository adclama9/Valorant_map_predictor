from PIL import Image
from PIL import ImageGrab
import torch
import os
import cv2  
import numpy as np
from torchvision import datasets, models, transforms
import time 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import sys
import keyboard

twokbbox = (86,77,535,549)
onekbbox = (65,60,401,412)
x = ['Green','Red']
working_directory = os.getcwd()
path = working_directory+"/models/model_best_resnet150_v2.pth"
model = torch.load(path)
model.to("cpu")
model.eval()
plt.ion()


def test_live(bbox , mask):
    
    #populating graph with 0's so that theres 50 points to show 
    timelist = [0]*50
    greenlist = [0]*50
    redlist = [0]*50
        
    while True:
        #screen capturing the map and filtering with mask 
        printscreen = np.array(ImageGrab.grab(bbox=bbox))
        masked_image = cv2.bitwise_and(cv2.cvtColor(printscreen,cv2.COLOR_BGR2RGB), mask)
        masked_image = Image.fromarray(masked_image) # CONVERT BACK TO PIL TYPE FOR MODEL
        
        #process to trained format 
        preprocess = transforms.Compose([
        transforms.Resize((128,128)),transforms.ToTensor()
        ])
        img_map_preprocessed = preprocess(masked_image)
        img_tensor = torch.unsqueeze(img_map_preprocessed,0)
        #do prediction
        output = model(img_tensor)
        
        #jank add data to list to plot
        timelist.append(time.time())
        greenlist.append(output[0][0].detach().numpy())
        redlist.append(output[0][1].detach().numpy())
        
        greenlist.pop(0)
        redlist.pop(0)
        timelist.pop(0)
       
        plt.plot(timelist, greenlist, label = "Green Team", linewidth=3 , color = 'green')
        plt.plot(timelist, redlist, label = "Red Team", linewidth=3, color = 'red')  
        plt.xlabel("Time")
        plt.ylabel("Confidence level")
        plt.draw()
        plt.pause(0.2)
        plt.clf()
        
        #adding close graph key
        

def main():
    mask = cv2.imread('bw.png')
    while True:
        res  = int (input("Press 1 for 1080p \nPress 2 for 1440p\n"))
        if res == 1:
            bbox = onekbbox
            mask = cv2.resize(mask, dsize=(336, 352), interpolation=cv2.INTER_CUBIC)
            break
        elif res == 2:
            bbox = twokbbox
            break
        else:
            print("Incorrect input detected, try again")
    
    
    temp = test_live(bbox,mask)
    return('Done')
    
#old function to teset processing image
def test_image():
    path = working_directory+"/after_images/train/r/r1651025726.076507.png"
    
    mappic = Image.open(path)
    #def predict(path):
    preprocess = transforms.Compose([
        transforms.Resize((128,128)),transforms.ToTensor()
        
        ])

    img_map_preprocessed = preprocess(mappic)
    img_tensor = torch.unsqueeze(img_map_preprocessed,0)

    output = model(img_tensor)
    print (output)
    
    
# old function to test model outputting the results in number format
def test_live_num(fluff=None):

    while True:
        printscreen = np.array(ImageGrab.grab(bbox=(86,77,535,549)))
        masked_image = cv2.bitwise_and(cv2.cvtColor(printscreen,cv2.COLOR_BGR2RGB), mask)
        #cv2.imshow('window1',masked_image)
        masked_image = Image.fromarray(masked_image) # CONVERT BACK TO PIL TYPE FOR MODEL
        preprocess = transforms.Compose([
        transforms.Resize((128,128)),transforms.ToTensor()
        ])

        img_map_preprocessed = preprocess(masked_image)
        img_tensor = torch.unsqueeze(img_map_preprocessed,0)
        output = model(img_tensor)
        #y = output[0][0].detach().numpy(), output[0][1].detach().numpy()
        print("Green : ",output[0][0].detach().numpy() , " Red : " , output[0][1].detach().numpy())
        
        
   

if __name__ == "__main__":
    main()
