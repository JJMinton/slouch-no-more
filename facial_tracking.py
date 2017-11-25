#!/bin/python3.6
import requests, json

import keys


from webcam import get_image


def should_analyze(image):
    return True


def analyze_image(image_data):
    try:
        # Execute the REST API call and get the response.
        response = requests.request('POST', keys.url_face, files={}, data=image_data, headers=headers, params=params)
        parsed = json.loads(response.text)
        return parsed

    except Exception as e:
        print('Error:')
        print(e)


def process_result(result):
    print ('Response:')
    print (json.dumps(result, sort_keys=True, indent=2))

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
