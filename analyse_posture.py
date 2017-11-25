#!/bin/python3.6
import json

def analyse_posture(result):
    print ('Response:')
    print (json.dumps(result, sort_keys=True, indent=2))
    return True
