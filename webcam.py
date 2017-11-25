import cv2
from time import sleep

#from facial_tracking import


def get_image():

    #cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        sleep(.1) # Allow camera to calibrate exposure
        rval, frame = vc.read()
    else:
        rval = False

    #while rval:
    #    cv2.imshow("preview", frame)
    #    rval, frame = vc.read()
    #    key = cv2.waitKey(20)
    #    if key == 27: # exit on ESC
    #        break
    #cv2.destroyWindow("preview")

    vc.release()

    cv2.imwrite("test.png", frame)

    return frame #TODO: change to byte stream



if __name__ == "__main__":

    frame = get_frame()
    print(type(frame))
    cv2.imwrite("test.png", frame)
