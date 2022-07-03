import cv2 as cv
import numpy as np
import pytesseract

import cropping, util
import sanity_checking as sc

# define configs for pytesseract
int_config = r'-c tessedit_char_whitelist=0123456789 --psm 10'
float_config = r'-c tessedit_char_whitelist=0123456789. --psm 10'

# define indices where float is needed
game_float_indices = [2, 20]
player_float_indices = [0, 16, 17]


def set_tesseract_path(path='C:\\Program Files\\Tesseract-OCR\\tesseract'):
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
            data.append(get_number_from_image(np.array(images[i]), config=float_config))
        else:
            data.append(get_number_from_image(np.array(images[i])))

    game_dict = get_game_dict(data)
    sc.check_game_sanity(game_dict)

    return game_dict


def get_player_data(screenshot, name=""):
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
    images = cropping.crop_player_data(screenshot)
    data = []

    for i in range(len(images)-1):
        if i in player_float_indices:
            data.append(get_number_from_image(np.array(images[i]), config=float_config))
        else:
            data.append(get_number_from_image(np.array(images[i])))

    data.extend(get_card_data(images[18]))

    return get_player_dict(data, name)


def get_number_from_image(img, max_reads_per_size=10, max_resize_factor=5, equal_reads_to_accept=3, config=int_config):
    """
    Reads an image that should only contain a single line of numbers and returns the result as a string.
    The image will be resized if the result is unclear. For every resize a max number of reads are performed.
    In order to accept the result a number of equal reads must be achieved. An unsuccessful read returns '-1'.

    Parameters:
        img(iamge): the image to read
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


def get_game_dict(data):
    """
    Stores the data from a game given as a list in a dictionary.

    Parameters: 
        data(list): data to pass into dictionary

    Returns:
        game_dict(dict): dictionary with the data
    """
    half_length = int(len(data)/2)

    game_dict = {
        "Possession": [int(data[0]), int(data[0+half_length])],
        "Shots": [int(data[1]), int(data[1+half_length])],
        "ExpectedGoals": [float(data[2]), float(data[2+half_length])],
        "Passes": [int(data[3]), int(data[3+half_length])],
        "Tackles": [int(data[4]), int(data[4+half_length])],
        "TacklesWon": [int(data[5]), int(data[5+half_length])],
        "Interceptions": [int(data[6]), int(data[6+half_length])],
        "Saves": [int(data[7]), int(data[7+half_length])],
        "FoulsCommitted": [int(data[8]), int(data[8+half_length])],
        "Offsides": [int(data[9]), int(data[9+half_length])],
        "Corners": [int(data[10]), int(data[10+half_length])],
        "FreeKicks": [int(data[11]), int(data[11+half_length])],
        "PenaltyKicks": [int(data[12]), int(data[12+half_length])],
        "YellowCards": [int(data[13]), int(data[13+half_length])],
        "RedCards": [int(data[14]), int(data[14+half_length])],
        "DribbleSuccessRate": [int(data[15]), int(data[15+half_length])],
        "ShotAccuracy": [int(data[16]), int(data[16+half_length])],
        "PassAccuracy": [int(data[17]), int(data[17+half_length])]
    }

    return game_dict


def get_player_dict(data, name):
    """
    Stores the data from a player given as a list in a dictionary.

    Parameters:
        data(list): data to pass into dictionary
        name(string): name of the player

    Returns:
        player_dict(dict): dictionary with the data
    """

    player_dict = {
        "Name": name,
        "Rating": float(data[0]),
        "Goals": int(data[1]),
        "Assists": int(data[2]),
        "Shots": int(data[3]),
        "ShotAccuracy": int(data[4]),
        "Passes": int(data[5]),
        "PassAccuracy": int(data[6]),
        "Dribbles": int(data[7]),
        "DribbleSuccessRate": int(data[8]),
        "Tackles": int(data[9]),
        "TackleSuccessRate": int(data[10]),
        "Offsides": int(data[11]),
        "FoulsCommitted": int(data[12]),
        "PossessionWon": int(data[13]),
        "PossessionLost": int(data[14]),
        "MinutesPlayed": int(data[15]),
        "DistanceCovered": float(data[16]),
        "DistanceSprinted": float(data[17]),
        "YellowCard": int(data[18]),
        "RedCard": int(data[19])
    }

    return player_dict


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
