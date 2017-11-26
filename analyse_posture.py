#!/bin/python3.6
import json


class PostureAnalyser():
    def __init__(self):
        self.yaw = None
        self.pitch = None
        self.roll = None
        self.x = None
        self.y = None

        self.delta_yaw = 13
        self.delta_pitch = 3
        self.delta_roll = 8

        self.delta_x = 50
        self.delta_y = 20


    def configure(self, result):
        if result:
            self.yaw = result[0]["faceAttributes"]["headPose"]["yaw"]
            self.pitch = result[0]["faceAttributes"]["headPose"]["pitch"]
            self.roll = result[0]["faceAttributes"]["headPose"]["roll"]

            self.x = result[0]["faceLandmarks"]["noseTip"]["x"]
            self.y = result[0]["faceLandmarks"]["noseTip"]["y"]
        return True

    def analyse_posture(self, result):
        if result:
            try:
                yaw = result[0]["faceAttributes"]["headPose"]["yaw"]
                pitch = result[0]["faceAttributes"]["headPose"]["pitch"]
                roll = result[0]["faceAttributes"]["headPose"]["roll"]

                x = result[0]["faceLandmarks"]["noseTip"]["x"]
                y = result[0]["faceLandmarks"]["noseTip"]["y"]
            except KeyError:
                print(result)
                raise

            if self.x is None:
                return self.configure(result)
                
            #horizontal movement is fine
            #if abs(x-self.x) > self.delta_x:
            #    return False
            if y > self.y + self.delta_y: #y is from top of frame
                return False
            if abs(yaw-self.yaw) > self.delta_yaw:
                return False
            if abs(pitch-self.pitch) > self.delta_pitch:
                return False
            if abs(roll-self.roll) > self.delta_roll:
                return False

            return True
                
        else:
            print ('Response:')
            print (json.dumps(result, sort_keys=True, indent=2))
            return True
