#!/bin/python3.6
import json

def analyise_posture(result):
    print ('Response:')
    print (json.dumps(result, sort_keys=True, indent=2))

