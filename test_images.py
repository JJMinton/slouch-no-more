#!/bin/python3.6

def get_image(image=1):
    with open('images/test{}.jpg'.format(image), 'rb') as f:
        data = f.read()
    return data
