#!/bin/python3.6

import io
import queue
from multiprocessing import Process
import threading
import time

### Tkinter stuff
from itertools import cycle
import tkinter as tk
from PIL import Image, ImageTk

import config

#### Image processing
from webcam_pygame import get_image
#from test_images import get_image
from api_call import make_api_call
from analyse_posture import PostureAnalyser



class GuiApplication(tk.Frame):
    def __init__(self, master, width, height, queue):
        tk.Frame.__init__(self, master)
        self.queue = queue
        self.posture = PostureAnalyser()
        self.width, self.height = width, height
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
        print('called updateImage')
        print(self.queue.qsize())
        while self.queue.qsize():
            try:
                print('updating image')
                image_path, results = self.queue.get(0)

                posture = self.posture.analyse_posture(results) 
                if  posture == 'resources/neutral.png':
                    self.can.config(bg="grey")
                else:
                    self.can.config(bg="red")
                img = Image.open(posture)
                self.warning_pic = ImageTk.PhotoImage(img)
                self.warning.config(image=self.warning_pic)

                if results:
                    self.ypr.set('Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}'.format(**results[0]['faceAttributes']["headPose"]))
                    self.xy.set('Nose tip (x,y): ({x}, {y})'.format(**results[0]["faceLandmarks"]["noseTip"]))
                else:
                    self.ypr.set('Yaw: -, Pitch: -, Roll: -')
                    self.xy.set('Nose tip (x,y): (-, -)')

                img = Image.open(image_path)
                self.drawImage(img)


            except queue.Empty:
                pass

    def drawImage(self, image):
        ### Resize image to fit in box
        x,y, width, height = image.getbbox()
        factor = min(self.width / (width-x), self.height / (height-y))
        width, height = int((width-x)*factor), int((height-y)*factor)
        img = image.resize((width, height)).transpose(Image.FLIP_LEFT_RIGHT)

        #Draw image
        self.pic = ImageTk.PhotoImage(img)
        self.item = self.can.create_image(width/2,height/2, image=self.pic) 


class ThreadedClient:

    def __init__(self, master):
        self.stop = False
        self.master = master
        self.queue = queue.Queue()
        self.gui = GuiApplication(master, config.width, config.height, self.queue)

        #Threading
        self.process1 = threading.Thread(target = self.process_images)
        self.process1.start()

        self.periodicCall()

    def periodicCall(self):
        if self.stop:
            import sys
            sys.exit(1)
        self.gui.updateImage()
        self.master.after(config.delay*1000, self.periodicCall)

    def process_images(self): #TODO: make asyncronous to increase pushing to queue

        async def make_call():
            image_path = get_image()
            yield from make_api_call(image_path)
            
        def callback(image_path, results):
            self.gui.queue.put((image_path, results))
            print(self.gui.queue.qsize())

        async def async_main(loop):
            while not self.stop:
                asyncio.ensure_future(make_call())
                make call on future
                await asyncio.sleep(config.delay)
                
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_main(loop))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")

    client = ThreadedClient(root)

    root.mainloop()
