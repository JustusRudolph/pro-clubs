import cv2 as cv
import numpy as np
import pytesseract

from vision import cropping, util
from vision import dict_creater as dc

# define configs for pytesseract
int_config = r'-c tessedit_char_whitelist=0123456789 --psm 10'
float_config = r'-c tessedit_char_whitelist=0123456789. --psm 10'

# define indices where float is needed
game_float_indices = [2, 20]
player_float_indices = [0, 16, 17, 21, 41]


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
    data = []

    for i in range(len(images)):
        if i in game_float_indices:
            data.append(float(get_number_from_image(np.array(images[i]), config=float_config)))
        else:
            data.append(int(get_number_from_image(np.array(images[i]))))

    return dc.get_game_dict(data)


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
    data = []

    for i in range(len(images)):
        if i==18: # index of image with card area
            data.extend(get_card_data(images[i]))
        elif i in player_float_indices:
            data.append(float(get_number_from_image(np.array(images[i]), config=float_config)))
        else:
            data.append(int(get_number_from_image(np.array(images[i]))))

    return dc.get_player_dict(data, name)


def get_number_from_image(img, max_reads_per_size=10, max_resize_factor=5, equal_reads_to_accept=3, config=int_config):
    """
    Reads an image that should only contain a single line of numbers and returns the result as a string.
    The image will be resized if the result is unclear. For every resize a max number of reads are performed.
    In order to accept the result a number of equal reads must be achieved. An unsuccessful read returns '-1'.

    Parameters:
        img(image): the image to read
        max_reads_per_size(int): max reads per resize
        max_resize_factor(int): max resizes
        equal_reads_to_accept(int): number of equals reads the accept the result
        config(string): custom config for tesseract
    
    Returns:
        numbers(string): numbers from image
    """
    height, width, channels = img.shape

    # uncomment to apply grayscale and thresholding filter - might improve performance
    # image = util.get_grayscale(image)
    # image = util.thresholding(image)

    for size_factor in range(max_resize_factor):
        start_size = 1
        image_resized = cv.resize(img, (width * (size_factor + start_size), height * (size_factor + start_size)))

        equal_reads = 1
        last_read = ""
        for i in range(max_reads_per_size):
            number = pytesseract.pytesseract.image_to_string(image_resized, config=config)
            number = number.split()

            if len(number) == 0:
                break
            else:
                # check if first character is a dot
                if util.split(number[0])[0] == '.':
                    continue
                # check if the first character is '0' and the following character is not '.' or '0',
                # then the read was invalid
                if len(util.split(number[0])) > 1:
                    if util.split(number[0])[0] == '0' and util.split(number[0])[1] != '.'\
                            and util.split(number[0])[1] != '0':
                        continue
                if last_read != number[0]:
                    last_read = number[0]
                    equal_reads = 1
                else:
                    equal_reads += 1

            if equal_reads >= equal_reads_to_accept:
                return last_read

    return "-1"


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
