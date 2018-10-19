import random

from analyse_posture import Posture

def get_posture(image_path):
    if random.random() < 0.05:
        return None
    return Posture(
        random.normalvariate(0.0, 3.), # yaw
        random.normalvariate(0.0, 3.), # pitch
        random.normalvariate(0.0, 3.), # roll
        random.normalvariate(0.0, 10.), # height
        random.normalvariate(0.0, 10.), # lean
    )
