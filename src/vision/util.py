import pyautogui
import pygetwindow
import time
import cv2 as cv
import numpy as np


def take_screenshot(title, wait_time):
    """
    Opens the application with the given window title, waits a certain amount of time and then takes a screenshot.

    Parameters:
        title(string): application title to take screenshot from
        wait_time(float): time in seconds to wait before screenshot is taken

    Returns:
        screenshot(image): the taken screenshot
    """
    # not working
    # window = pygetwindow.getWindowsWithTitle(title)[0]
    # window.activate()
    time.sleep(wait_time)
    screenshot = pyautogui.screenshot()
    return screenshot

def get_main_color(img):
    """
    Parameters:
        img(image): image to check for main color

    Returns:
        main_color(tuple): main color of image in rgb format
    """
    colors = img.getcolors(256)  # put a higher value if there are many colors in your image
    max_occurrence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurrence:
                (max_occurrence, most_present) = c
        return most_present
    except TypeError:
        raise Exception("Too many colors in the image")


# split word into list of its characters
def split(word):
    return [char for char in word]


# get grayscale image
def get_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv.morphologyEx(image, cv.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv.warpAffine(image, M, (w, h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
