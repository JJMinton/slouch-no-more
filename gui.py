#!/bin/python3.6

import io
import pygame

### Tkinter stuff
from itertools import cycle
import tkinter as tk
from PIL import Image, ImageTk

#### Image processing
from image_pygame import get_image
#from test_images import get_image
from posture_opencv import get_posture
from analyse_posture import PostureAnalyser


class Application(tk.Frame):
    def __init__(self, master, width, height):
        tk.Frame.__init__(self, master)
        self.posture = PostureAnalyser()
        self.width, self.height = width, height

        # load sounds
        self.sounda = None
        try:
            pygame.init()
            pygame.mixer.init()
            self.sounda = pygame.mixer.Sound('resources/sound.wav')
        except pygame.error:
            pass

        self.grid()
        self.createWidgets()
        self.updateImage()
        
    def createWidgets(self):
        self.can = tk.Canvas(root, width=self.width, height=self.height)
        self.can.grid(row=0)

        self.warning = tk.Label()
        self.warning.grid(row=0,column=1)

        self.ypr = tk.StringVar()
        self.ypr_label = tk.Label(root, textvariable = self.ypr)
        self.ypr_label.grid(row=1)

        self.xy = tk.StringVar()
        self.xy_label = tk.Label(root, textvariable = self.xy)
        self.xy_label.grid(row=1, column=1)


    def updateImage(self):
        image_path = get_image()
        posture = get_posture(image_path)

        # process image
        if posture:
            advice = self.posture.analyse_posture(posture) 
        else:
            advice = 'resources/neutral.png'

        self.can.config(bg="red")
        if self.sounda:
            # self.sounda.stop()
            self.sounda.play()

        img = Image.open(advice)
        self.warning_pic = ImageTk.PhotoImage(img)
        self.warning.config(image=self.warning_pic)

        if posture:
            self.ypr.set('Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}'.format(**posture._asdict()))
            self.xy.set('Lean: {lean}, Height: {height}'.format(**posture._asdict()))
        else:
            self.ypr.set('Yaw: -, Pitch: -, Roll: -')
            self.xy.set('Lean: -, Height: -')

        img = Image.open(image_path)
        self.drawImage(img)
        self.after(1, self.updateImage)

    def drawImage(self, image):
        ### Resize image to fit in box
        x,y, width, height = image.getbbox()
        factor = min(self.width / (width-x), self.height / (height-y))
        width, height = int((width-x)*factor), int((height-y)*factor)
        img = image.resize((width, height)).transpose(Image.FLIP_LEFT_RIGHT)

        #Draw image
        self.pic = ImageTk.PhotoImage(img)
        self.item = self.can.create_image(width/2,height/2, image=self.pic) 



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x600")
    root.title('Slouch No More!')

    image_numbers = cycle(range(10))

    app = Application(root, 300, 300)

    root.mainloop()
