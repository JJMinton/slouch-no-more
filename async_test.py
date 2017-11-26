import config

import asyncio
import queue
import time

from webcam_pygame import get_image
#from test_images import get_image
from api_call import make_api_call
from analyse_posture import PostureAnalyser


queue = queue.Queue()

#def get_image():
    #import random
    #name = ''.join(random.sample(set('abcdefghijklmnopqrstuvwxyz'), 5))
    #return name

#def make_api_call(image_path):
    #asyncio.sleep(3)
    #return 0

def make_call(future, loop):
    print('getting image...')
    image_path = get_image()
    print('making call...')
    result = make_api_call(image_path)
    future.set_result((image_path, result))
    print('image_name: {}'.format(future.result()[0]))
    
def callback(future):
    image_path, results = future.result()
    queue.put((image_path, results))
    print('queue size: {}'.format(queue.qsize()))

        
loop = asyncio.get_event_loop()
while True:
    future = asyncio.Future()
    future.add_done_callback(callback)
    print('calling')
    loop.call_soon(make_call(future, loop))
    #loop.run_until_complete(asyncio.sleep(1))
#loop.run_until_complete(async_main(loop))
