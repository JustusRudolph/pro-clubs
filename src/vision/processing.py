from PIL import ImageOps
import cv2 as cv
import numpy as np
import pytesseract, os, sys

import cropping, util

cwd = os.getcwd()
parent = os.path.dirname(cwd)
sys.path.insert(0, parent) 

from static_data import vision_static_data as vst

# set path to traineddata for teseract
os.environ['TESSDATA_PREFIX'] = './tess_traineddata'

# define configs for pytesseract
PYTESS_INT_CONFIG = r'-c tessedit_char_whitelist=0123456789 --psm 10'
PYTESS_FLOAT_CONFIG = r'-c tessedit_char_whitelist=0123456789. --psm 10'

# define indices where float is needed
GAME_FLOAT_INDICES = [2, 20]
PLAYER_FLOAT_INDICES = [0, 16, 17, 20, 40]

PLAYER_CARD_IMAGE_INDEX = 52 # index of image with card area


def set_tesseract_path(path):
    """
    Sets the tesseract path through the given absolute path.
    """
    pytesseract.pytesseract.tesseract_cmd = path


def get_game_data(screenshot):
    """
    Takes a screenshot taken in the match facts screen, then crops the data from the screenshot
    and reads the data with pytesseract. The data is stored in a dictionary on which a
    'sanity check' is performed to filter out unlogical values. Unlogical values are marked by setting
    them to -1.

    Parameters:
        screenshot(image): screenshot taken in the match facts screen

    Returns:
        game_dict(dict): dictionary that contains all relevant data from the match facts screen
    """
    images = cropping.crop_game_data(screenshot)
    attributes = list(vst.game_exp_range_dict.keys())

    data = []
    misreads = []

    for i in range(len(images)):
        img = ImageOps.invert(images[i])
        attribute = attributes[i % len(attributes)]

        if i in GAME_FLOAT_INDICES:
            data.append(float(get_number_from_image(np.array(img), attribute, player=False, config=PYTESS_FLOAT_CONFIG)))
        else:
            data.append(int(get_number_from_image(np.array(img), attribute, player=False)))

        if data[i] == -1:
            if i < len(attributes):
                team = 0
            else:
                team = 1
            misreads.append((team, attribute))

    game_dict = {}
    attribute_list = list(vst.game_exp_range_dict.keys())

    for i in range(len(attribute_list)):
        key = attribute_list[i]

        value_home = data[i]
        value_away = data[i + len(attributes)]

        game_dict[key] = [value_home, value_away]

    return game_dict, misreads


def get_player_data(screenshots, name=""):
    """
    Takes a screenshot taken in the player performance screen, then crops the data from the screenshot
    and reads the data with pytesseract. The data is stored in a dictionary on which a
    'sanity check' is performed to filter out unlogical values. Unlogical values are marked by setting
    them to -1. A name can be passed to set the player name in the dictionary.

    Parameters:
        screenshot(image): screenshot taken in the player performance screen
        name(string): name of the player to store in the dictionary

    Returns:
        player_dict(dict): dictionary that contains all relevant data from the player performance screen
    """
    images = cropping.crop_player_data(screenshots)
    attributes = list(vst.player_exp_range_dict.keys())

    misreads = []
    player_dict = {}
    player_dict["Name"] = name

    for i in range(len(images)):
        attribute = attributes[i]

        if i==PLAYER_CARD_IMAGE_INDEX: 
            data = get_card_data(images[i]) # returned as ints in a list
            player_dict[attribute] = data[0]
            player_dict[attributes[i+1]] = data[1]
            continue

        img = ImageOps.invert(images[i])
        
        if i in PLAYER_FLOAT_INDICES:
            data = float(get_number_from_image(np.array(img), attribute, config=PYTESS_FLOAT_CONFIG))
        else:
            data = int(get_number_from_image(np.array(img), attribute))

        if data == -1:
            misreads.append((name, attribute))

        player_dict[attribute] = data

    return player_dict, misreads


def get_number_from_image(img, attribute, player=True, config=PYTESS_INT_CONFIG, filters=False):
    """
    Reads an image that should only contain a single line of numbers and returns the result as a string.
    The image will be resized if the result is unclear. For every resize a max number of reads are performed.
    In order to accept the result a number of equal reads must be achieved. An unsuccessful read returns '-1'.

    Parameters:
        img(image): the image to read
        attribute(string): which attribute is read from the image
        player(bool): if the attribute belongs to the player screen, if not its the match screen
        config(string): custom config for pytesseract
        filters(bool): if additional filters should be applied (grayscale and thresholding)
    
    Returns:
        number(string): number from image
    """
    height, width, channels = img.shape

    # apply grayscale and thresholding filter if wanted, may improve accuracy
    if filters:
        img = util.get_grayscale(img)
        img = util.thresholding(img)

    number = pytesseract.pytesseract.image_to_string(img, config=config, lang='digits') # TODO: different path for digits data
    number = number.split()

    if len(number) == 0 or not check_expected_range(float(number[0]), attribute, player):
        for resize_factor in range(2, 5):
            img_resized = cv.resize(img, (width * resize_factor, height * resize_factor))

            number = pytesseract.pytesseract.image_to_string(img_resized, config=config, lang='eng')
            number = number.split()

            if len(number) == 0:
                continue

            if check_expected_range(float(number[0]), attribute, player):
                return number[0]

        return "-1"

    return number[0]


def check_expected_range(value, key, player):
    if player:
        exp_range = vst.player_exp_range_dict[key]
    else:
        exp_range = vst.game_exp_range_dict[key]

    return (exp_range[0] <= value <= exp_range[1])


def get_card_data(img):
    """
    Checks if a player has received a card during the game by checking the area
    where the card is displayed for its main color.


    Parameters:
        img(image): image that contains the area of the card

    Returns:
        res(list): list that says whether a player has a yellow or red card
    """
    main_color = util.get_main_color(img)

    if main_color[0] < 100:
        return [0, 0]
    elif main_color[0] < 200:
        return [0, 1]
    else:
        return [1, 0]
