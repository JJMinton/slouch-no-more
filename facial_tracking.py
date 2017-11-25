#!/bin/python3.6
import requests, json

import keys


def should_analyze(image):
    return True

def get_image():
    with open('images/test1.jpg', 'rb') as f:
        data = f.read()
    return data
    
def analyze_image(image_data):
    try:
        # Execute the REST API call and get the response.
        response = requests.request('POST', uri_base, files={}, data=image_data, headers=headers, params=params)
        headPose = response.json()[0]['faceAttributes']['headPose']
        return headPose

    except Exception as e:
        print('Error:')
        print(e)
    

def process_result(result):
    pitch = headPose['pitch']
    roll = headPose['roll']
    yaw = headPose['yaw']

if __name__ == "__main__":

    # Request headers.
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': keys.key_face,
    }

    # Request parameters.
    params = {
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'true',
        'returnFaceAttributes': 'headPose,emotion',
        #'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }
    
    i=0
    while i < 4:
        i += 1
        image = get_image()
        if should_analyze(image):
            result = analyze_image(image)
            process_result(result)

