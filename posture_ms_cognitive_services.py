#!/bin/python3.6
import requests, json
import keys

from analyse_posture import Posture

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
    
def get_posture(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    try:
        # Execute the REST API call and get the response.
        response = requests.request('POST', keys.url_face, files={}, data=image_data, headers=headers, params=params)
        result = json.loads(response.text)
        if result:
            try: 
                posture = Posture(
                    result[0]["faceAttributes"]["headPose"]["yaw"],
                    result[0]["faceAttributes"]["headPose"]["pitch"],
                    result[0]["faceAttributes"]["headPose"]["roll"],
                    result[0]["faceLandmarks"]["noseTip"]["y"],
                    result[0]["faceLandmarks"]["noseTip"]["x"],
                )
                return posture
            except KeyError as e:
                print('Error:')
                print(e)
                print ('Response:')
                print (json.dumps(result, sort_keys=True, indent=2))
    except Exception as e:
        print('Error:')
        print(e)
    return None
