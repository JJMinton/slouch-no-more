from pygame import camera, image
from time import sleep

camera.init()
cam = camera.Camera("/dev/video0", (640, 480));
cam.start()


def get_image():

    sleep(.1) # Allow camera to calibrate exposure
    im = cam.get_image()
    image.save(im, "images/temp_img.jpg")


    return 'images/temp_img.jpg'



if __name__ == "__main__":

    frame = get_image()
    #print(frame.tobytes())
    #cv2.imwrite("test.png", frame)
