#!/bin/python3.6

import io

### Tkinter stuff
from itertools import cycle
import tkinter as tk
from PIL import Image, ImageTk

#### Image processing
#from webcam import get_image
from test_images import get_image
from api_call import make_api_call
from analyse_posture import analyse_posture


class Application(tk.Frame):
    def __init__(self, master, width, height):
        tk.Frame.__init__(self, master)
        self.width, self.height = width, height
        self.grid()
        self.createWidgets()
        self.updateImage()
        
    def createWidgets(self):
        self.can = tk.Canvas(root, width=self.width, height=self.height)
        self.can.grid()


    def updateImage(self):
        image_binary = get_image()
        results = make_api_call(image_binary)

        if analyse_posture(results):
            print('good posture')
            self.config(bg='grey')
        else:
            print('bad posture')
            self.config(bg='red')


        img = Image.open(io.BytesIO(image_binary))
        self.drawImage(img)
        self.after(1000, self.updateImage)

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

    app = Application(root, 500, 500)

    root.mainloop()
