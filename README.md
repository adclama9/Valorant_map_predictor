# Valorant Round Win Predictor
This repo goes through the methodology I took.

Main idea:
Have a live feed of a map that can predict the chance of a team winning based on the positioning on the map.
Trying with the Ascent map.

Steps:
1. Acquire data from masters vods
2. Train CNN on the data
3. Try on live feed

## Data Collection (get_data.py, manual_get_data.py)
To get the data for our training, I had to go through vods from Masters Reykjavik 2022.
The vods look like this.
![image](https://user-images.githubusercontent.com/57018666/169892769-960e7e0a-60bb-4053-969a-ea1efa7aec10.png)

What I want is just the image of the map.
![image](https://user-images.githubusercontent.com/57018666/169893106-e3d20090-bd1a-4b20-9f71-7cdcf153a2c4.png)

But I also want to automataically capture just the map.
In order to automate the collection of images, I wrote a program to read the rounds.
The logic for the automation is:
1. Capture map every half second.
2. If either the green or red teams score go up by 1, save all the images to the correct folder (green or red folder).
3. Wait 30 seconds for the pre-round to end.
4. Repeat.

### Filtering the map
In order to only capture the map, I had to filter out the map.
Below is an attempt to use Otsu and other methods to filter out just the map.
![image](https://user-images.githubusercontent.com/57018666/164949137-f8082cd2-da5b-4f6c-839d-e6de33e20f1f.png)
But it doesn't apply super well to a video and the details are all gone.

So instead I created a layer and just put it over the map while capturing.
![bw](https://user-images.githubusercontent.com/57018666/169893795-20cc8f27-c52b-4bb4-8176-7a85e5c765f4.png)

Combined with a screen capture, it gets what I want.
![g1651025520 061634](https://user-images.githubusercontent.com/57018666/169894372-a4e6ea4e-ca28-404f-99f8-c39618c06faa.png)


### Counting the rounds
For counting the rounds, all I care about is the scores from the vod
![image](https://user-images.githubusercontent.com/57018666/169894206-ffa51b98-771e-47a6-b0b5-91f908a2a121.png)
I needed a way to automatically read it, so i put a screen capture on the two areas
The idea is to use PyTesseract, an optical character recognition package, to read an image and get the number from it.
Originally the screencapture looked like this:
![num3](https://user-images.githubusercontent.com/57018666/169894823-6fa58153-08c8-46d8-8745-2c375d4b22b2.png)
But the program wasn't recognizing it well, so I had to use Otsu's method again to flip it and make it clearer.
![image](https://user-images.githubusercontent.com/57018666/169894807-b5cef5e6-38ef-4f1a-8d4e-8f74dfa0fd96.png)

#### Issues with this method
The problems came from Valorant using "Tungsten Narrow Black" Font. PyTesseract wasn't able to determine what some of the numbers were.
![image](https://user-images.githubusercontent.com/57018666/169895578-f0dbb53b-b3a9-44b6-91a3-34e76788a553.png)
![image](https://user-images.githubusercontent.com/57018666/169895653-347769c2-06eb-4d64-b831-4c8eb98568c5.png)
![image](https://user-images.githubusercontent.com/57018666/169895706-23eac90f-485d-4668-9877-52c1d9f8428e.png)

Numbers like 5,6,7 and 8 were extremely confusing for the OCR to determine correctly. 
I even tried to train Pytesseract on every number, yet it continued to fail.
![image](https://user-images.githubusercontent.com/57018666/169895826-b2ac3662-901f-4f2b-b529-78a7340f0949.png)

### Manually getting images
I ended up having a script that captured images every half second and saves the images to the folder that I tell it to depending on which keyboard button I was pressing. 
Going through every vod in Masters 1, I got roughly 4500 Images for training and 500 images for validation.

## Training the model (train_model_resnet152.ipynb)
tldr: Tried making my own CNN model but it didn't work. Decided to use untrained Resnet150 instead.
The model I decide to use was a CNN model since this is image classfication.
After weeks of failing to train it on my personal computer (Memory leaks,etc.), I ended up using Google Colab to train the model.
Decided to use an untrained ResNet152 since it's a CNN model that's built for classification (and it's popular).

I only tuned the learning rate using a LR-Finder.
![image](https://user-images.githubusercontent.com/57018666/170832612-073f394c-70ad-47ac-8eb2-9d0a5060d966.png)

Was able to achieve 99% accuracy on training set and 88.6% accuracy on validation set.
![image](https://user-images.githubusercontent.com/57018666/170832632-12c345a2-faa6-41d2-9373-3b7823205a6c.png)

## Running the model (run_model.py)
Added an option to choose between 1080p monitor and 1440p monitor. 
Just watch the game in full screen and run the program. 
I created a live line graph so that you can visualize which team is performing better (higher is better)
![image](https://user-images.githubusercontent.com/57018666/170833171-3d619a82-dbe0-434b-a3c0-205b4b28893e.png)
It will keep predicting over and over until the program is closed.

## Possible Improvements
1. More data : Add way more images
2. Add more images for more maps! (Took too long for me to add more)
3. hyperparameter tuning : I did'nt tune batch size, optimizer weights, etc.


## Known errors
1. Doesn't work well between rounds because it wasn't trained on that.
2. It was trained before Fade was allowed in Pro play, so if Fade is in the game it has mistakes.

#Try it out yourself!
(Model file is too big for github, message me and I can send you a google drive link to download it.)
Download all requirements in valmappredenv.yml
Download all files
run run_model.py in the folder. 
