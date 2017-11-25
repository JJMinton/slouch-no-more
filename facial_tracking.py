#!/bin/python3.6
import requests, json

import keys


from webcam import get_image
from api_call import make_api_call
from analyse_posture import analyse_posture


def should_analyse(image):
    return True


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
        if should_analyse(image):
            api_result = make_api_call(image)
            analyse_posture(api_result)
