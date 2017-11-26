#!/bin/python3.6

import io

### Tkinter stuff
from itertools import cycle
import tkinter as tk
from PIL import Image, ImageTk

#### Image processing
from webcam_pygame import get_image
#from test_images import get_image
from api_call import make_api_call
from analyse_posture import PostureAnalyser


class Application(tk.Frame):
    def __init__(self, master, width, height):
        tk.Frame.__init__(self, master)
        self.posture = PostureAnalyser()
        self.width, self.height = width, height
        self.grid()
        self.createWidgets()
        self.updateImage()
        
    def createWidgets(self):
        self.can = tk.Canvas(root, width=self.width, height=self.height)
        self.can.grid(row=0)
        self.ypr = tk.StringVar()
        self.ypr_label = tk.Label(root, textvariable = self.ypr)
        self.ypr_label.grid(row=1)

        self.xy = tk.StringVar()
        self.xy_label = tk.Label(root, textvariable = self.xy)
        self.xy_label.grid(row=1, column=1)


    def updateImage(self):
        image_path = get_image()
        print(image_path)
        results = make_api_call(image_path)



        if self.posture.analyse_posture(results):
            print('good posture')
            self.can.config(bg="grey")
        else:
            print('bad posture')
            self.can.config(bg="red")

        if results:
            self.ypr.set('Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}'.format(**results[0]['faceAttributes']["headPose"]))
            self.xy.set('Nose tip (x,y): ({x}, {y})'.format(**results[0]["faceLandmarks"]["noseTip"]))
        else:
            self.ypr.set('Yaw: -, Pitch: -, Roll: -')
            self.xy.set('Nose tip (x,y): (-, -)')

        img = Image.open(image_path)
        self.drawImage(img)
        self.after(1, self.updateImage)

    def drawImage(self, image):
        ### Resize image to fit in box
        x,y, width, height = image.getbbox()
        factor = min(self.width / (width-x), self.height / (height-y))
        width, height = int((width-x)*factor), int((height-y)*factor)
        img = image.resize((width, height))

        #Draw image
        self.pic = ImageTk.PhotoImage(img)
        self.item = self.can.create_image(width/2,height/2, image=self.pic) 

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")

    image_numbers = cycle(range(10))

    app = Application(root, 300, 300)

    root.mainloop()
