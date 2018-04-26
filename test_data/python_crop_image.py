# Original code stolen from https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
# import the necessary packages
import argparse
import cv2
import os
from scipy.misc import imresize
from skimage.io import imread, imsave, use_plugin
from math import floor, ceil

use_plugin("freeimage")

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
sel_rect_endpoint = [(0,0)]

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, sel_rect_endpoint

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        sel_rect_endpoint = [(x, y)]

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
image_skimage = imread(args["image"])
clone = image.copy()
clone_skimage = image_skimage.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

while True:
    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        #cv2.imshow("image", image)
        if not cropping:
            cv2.imshow('image', image)
        elif cropping and sel_rect_endpoint:
            image = clone.copy()
            rect_cpy = clone.copy()
            cv2.rectangle(rect_cpy, refPt[0], sel_rect_endpoint[0], (0, 255, 0), 1)
            cv2.imshow('image', rect_cpy)

        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    # if there are two reference points, then crop the region of interest
    # from the image and display it
    if len(refPt) == 2:
        roi = clone_skimage[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imshow("crop", roi)
        key = cv2.waitKey(0) & 0xFF

        print 'Press enter to save crop or press q to quit or press any other key to recrop.'

        if key == ord("\n"):  # If not enter.
            import random, string
            crop_name = os.path.basename(args["image"]).replace(".png", "_cropped-{}.png".format(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))))

            print '  Saving crop to {}'.format(crop_name)
            #cv2.imwrite(crop_name, roi)
            imsave(crop_name, roi)

            import warnings
            warnings.simplefilter(action='ignore', category=FutureWarning)
            #h, w, c = roi.shape
            h, w = roi.shape[0], roi.shape[1]
            min_dim = min(h,w)
            h_extra = float(h - min_dim) / 2
            w_extra = float(w - min_dim) / 2
            roi = roi[int(floor(h_extra)):int(h) - int(ceil(h_extra)), int(floor(w_extra)):int(w) - int(ceil(w_extra))]

            resize_dim = 224
            roi = imresize(roi, (resize_dim, resize_dim))
            crop_name_center = crop_name.replace(".png", "-center.png")

            print '  Saving ({}, {}) center crop to {}'.format(resize_dim, resize_dim, crop_name_center)
            #cv2.imwrite(crop_name.replace(".png", "-center.png"), roi)
            imsave(crop_name_center, roi)

            # close all open windows
            cv2.destroyAllWindows()
            break
        elif key == ord("q"):
            print '  Not saving crop.'
            # close all open windows
            cv2.destroyAllWindows()
            break
        else:
            print '  Not saving crop.'
            cv2.destroyWindow("crop")
            image = clone.copy()



