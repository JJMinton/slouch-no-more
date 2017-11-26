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
                self.configure(result)
            else:
                #horizontal movement is fine
                #if abs(x-self.x) > self.delta_x:
                #    return False
                if y > self.y + self.delta_y: #y is from top of frame
                    return 'resources/down.png'
                if roll > self.roll + self.delta_roll:
                    return 'resources/tilt_left.png'
                if roll < self.roll - self.delta_roll:
                    return 'resources/tilt_right.png'
                if yaw > self.yaw + self.delta_yaw:
                    return 'resources/twist_left.png'
                if yaw < self.yaw - self.delta_yaw:
                    return 'resources/twist_right.png'
                if (pitch-self.pitch) > self.delta_pitch: #Pitch is always zero
                    return False

        else:
            print ('Response:')
            print (json.dumps(result, sort_keys=True, indent=2))
        return 'resources/neutral.png'
