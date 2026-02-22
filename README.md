# Overview
A real-time interactive physics simulation controlled live by YouTube chat messages.

The program reads live chat messages, parses them into commands, and injects them into a physics world. Designed to handle large numbers of simultaneous user actions by asynchronously processing chat messages and feeding them to the simulation one at a time.

# Requirements
### - macOS (Might work on other operating systems, but currently only tested on macOS)
### - python 3.13+

# How to Run

## 1. Create a virtual environment
Navigate to the project directory and run
```console
python3 -m venv .venv
```

## 2. Install dependencies
In the same directory, run
```console
pip3 install -r requirements.txt
```

## 3. Run main.py
You must run the main.py file from the src directory
```console
cd src
```
Then run,
```console
python3 main.py
```

## 4. Stream to YouTube
If you want the simulation to actually be live, you must use your own streaming software to stream to YouTube. I would recommend OBS, but any software should work. After your stream is live, copy the url and use the console to open the stream and start streaming chat messages.

# Technologies Used
### - Pygame: Rendering and sound
### - Pymunk: Physics
### - Bidict: Bidirectional dictionary
### - Selenium: Webscraping YouTube live messages

# Console
When you run the project, a console will open, allowing easy control over the simulation. You can inject chat commands and enter your stream url.

<img width="606" height="558" alt="Console" src="https://github.com/user-attachments/assets/84514d94-f3ee-4a8e-95a5-8748be22c877" />

# Configuration Files
You can modify many parameters of the simulation by using the available .json files located in the src/data directory. Feel free to tweak the simulation however you like. Here is a list of configurable files:
### - config.json
### - biomes.json
### - materials.json
### - display.json
### - pickaxes.json
### - sounds.json

# Other Notes
For clean rendering, screen width and height should always be multiples of the block texture resolution times the camera size (Eg. 624x1248 with camera_size=13).
If this does not happen, block textures may appear choppy or distorted.

# Images
<img width="410" height="827" alt="Screen Shot 1" src="https://github.com/user-attachments/assets/17b22c9a-f243-428c-aba3-ae99dea4157c" />
<img width="413" height="830" alt="Screen Shot 2" src="https://github.com/user-attachments/assets/a332e56d-2aef-49a1-8b05-769083bc0e62" />
<img width="414" height="825" alt="Screen Shot 4" src="https://github.com/user-attachments/assets/a49c2e3b-b5b5-4ced-b700-2df20c7afd62" />
<img width="408" height="824" alt="Screen Shot 5" src="https://github.com/user-attachments/assets/4d6345cf-22a1-4b56-9122-80262b97e062" />

