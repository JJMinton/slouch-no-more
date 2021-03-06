import cv2
from time import sleep


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

    cv2.imwrite("images/temp_img.png", frame)


    return "images/temp_img.png"



if __name__ == "__main__":

    frame = get_image()
    #print(frame.tobytes())
    #cv2.imwrite("test.png", frame)
