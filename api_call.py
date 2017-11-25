#!/bin/python3.6
import requests, json
import keys

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
    
def make_api_call(image_data):
    try:
        # Execute the REST API call and get the response.
        response = requests.request('POST', keys.url_face, files={}, data=image_data, headers=headers, params=params)
        parsed = json.loads(response.text)
        return parsed

    except Exception as e:
        print('Error:')
        print(e)
