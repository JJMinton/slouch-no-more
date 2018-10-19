from collections import namedtuple
import json

Posture = namedtuple('Posture', ['yaw', 'pitch', 'roll', 'height', 'lean'])

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

        self.delta_lean = 50
        self.delta_height = 20


    def configure(self, posture):
        self.yaw = posture.yaw
        self.pitch = posture.pitch
        self.roll = posture.roll

        self.height = posture.height
        self.lean = posture.lean
        return self

    def analyse_posture(self, posture):
        if self.height is None:
            self.configure(posture)
        else:
            # ignore lean
            # if abs(posture.lean-self.lean) > self.delta_lean:
            #     return False
            if posture.height > self.height + self.delta_height: #y is from top of frame
                return 'resources/down.png'
            if posture.roll > self.roll + self.delta_roll:
                return 'resources/tilt_left.png'
            if posture.roll < self.roll - self.delta_roll:
                return 'resources/tilt_right.png'
            if posture.yaw > self.yaw + self.delta_yaw:
                return 'resources/twist_left.png'
            if posture.yaw < self.yaw - self.delta_yaw:
                return 'resources/twist_right.png'
            # ignore pitch as it is always zero 
            # if (posture.pitch-self.pitch) > self.delta_pitch:
            #     return False
        return None
