import numpy as np
import pytesseract
import cv2 as cv

import cropping, util

# only on windows: add pytesseract to path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

# define configs for pytesseract
int_config = r'-c tessedit_char_whitelist=0123456789 --psm 10'
float_config = r'-c tessedit_char_whitelist=0123456789. --psm 10'


def get_game_data():
    images = cropping.crop_game_data(util.take_screenshot('FIFA 22', 1))
    data = []

    for i in range(len(images)):
        if i == 2 or i == 20:
            data.append(get_number_from_image(np.array(images[i]), config=float_config))
        else:
            data.append(get_number_from_image(np.array(images[i])))

    return get_game_data_dict(data)


def get_player_data(name=""):
    images = cropping.crop_player_data(util.take_screenshot('FIFA 22', 1))
    data = []

    for i in range(len(images)-1):
        if i == 0 or i == 16 or i == 17:
            data.append(get_number_from_image(np.array(images[i]), config=float_config))
        else:
            data.append(get_number_from_image(np.array(images[i])))

    data.extend(get_card_data(images[18]))

    return get_player_data_dict(data, name)


def get_number_from_image(image, max_reads_per_size=10, max_resize_factor=5, equal_reads_to_accept=3, config=int_config):
    height, width, channels = image.shape

    # uncomment to apply grayscale and thresholding filter - might improve performance
    # image = util.get_grayscale(image)
    # image = util.thresholding(image)

    for size_factor in range(max_resize_factor):
        start_size = 1
        image_resized = cv.resize(image, (width * (size_factor + start_size), height * (size_factor + start_size)))

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


def get_game_data_dict(data):
    game_data_dict = {
        "Possession": [int(data[0]), int(data[18])],
        "Shots": [int(data[1]), int(data[19])],
        "ExpectedGoals": [float(data[2]), float(data[20])],
        "Passes": [int(data[3]), int(data[21])],
        "Tackles": [int(data[4]), int(data[22])],
        "TacklesWon": [int(data[5]), int(data[23])],
        "Interceptions": [int(data[6]), int(data[24])],
        "Saves": [int(data[7]), int(data[25])],
        "FoulsCommitted": [int(data[8]), int(data[26])],
        "Offsides": [int(data[9]), int(data[27])],
        "Corners": [int(data[10]), int(data[28])],
        "FreeKicks": [int(data[11]), int(data[29])],
        "PenaltyKicks": [int(data[12]), int(data[30])],
        "YellowCards": [int(data[13]), int(data[31])],
        "RedCards": [int(data[14]), int(data[32])],
        "DribbleSuccessRate": [int(data[15]), int(data[33])],
        "ShotAccuracy": [int(data[16]), int(data[34])],
        "PassAccuracy": [int(data[17]), int(data[35])]
    }

    return game_data_dict


def get_team_data_dict(team_data):
    team_data_dict = {
        "Possession": int(team_data[0]),
        "Shots": int(team_data[1]),
        "ExpectedGoals": float(team_data[2]),
        "Passes": int(team_data[3]),
        "Tackles": int(team_data[4]),
        "TacklesWon": int(team_data[5]),
        "Interceptions": int(team_data[6]),
        "Saves": int(team_data[7]),
        "FoulsCommitted": int(team_data[8]),
        "Offsides": int(team_data[9]),
        "Corners": int(team_data[10]),
        "FreeKicks": int(team_data[11]),
        "PenaltyKicks": int(team_data[12]),
        "YellowCards": int(team_data[13]),
        "RedCards": int(team_data[14]),
        "DribbleSuccessRate": int(team_data[15]),
        "ShotAccuracy": int(team_data[16]),
        "PassAccuracy": int(team_data[17])
    }

    return team_data_dict


def get_player_data_dict(data, name):
    player_data_dict = {
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

    return player_data_dict


def get_card_data(img):
    main_color = util.get_main_color(img)

    if main_color[0] < 100:
        return [0, 0]
    elif main_color[0] < 200:
        return [0, 1]
    else:
        return [1, 0]


