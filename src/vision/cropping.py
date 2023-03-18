# defines the position of the images
# position is given as a list in the following order: left, top, right, bottom
crop_data_dict = {
    "RATING": [3.45, 5.22, 3.13, 4.1],
    "NAME": [7.5, 5.5, 3.8, 4],
    "CARD_AREA": [6, 3.8, 5.9, 3.7],
    "PLAYER_SUMMARY": [1.12, 3.78, 1.08, 1.14],
    "PLAYER_SPECIFICS": [1.09, 3.3, 1.06, 1.14],
    "PLAYER_SPECIFICS_SCROLLED_DOWN": [1.09, 3.66, 1.06, 1.14],
    "HOME_DATA": [2.9, 4.35, 2.58, 1.1],
    "AWAY_DATA": [1.62, 4.35, 1.53, 1.1],
    "HOME_SIDE_DATA": [6.4, 4.85],
    "AWAY_SIDE_DATA": [1.27, 1.18]
}


def crop_game_data(screenshot):
    """
    Crops the game data from a screenshot taken in the match facts screen.
    Assumes the screenshot was taken in full screen and in the format 16:9.

    Parameters:
        screenshot(image): screenshot from the match facts screen

    Returns:
        images(list): cropped images of the game data
    """
    images = []
    images.extend(crop_team_data(screenshot, True))
    images.extend(crop_team_data(screenshot, False))

    return images


def crop_player_data(screenshots):
    """
    Crops the player data from a screenshot taken in the player performance screen.
    Assumes the screenshot was taken in full screen and in the format 16:9.

    Parameters:
        screenshot(image): screenshot from the player performance screen

    Returns:
        images(list): cropped images of the player data
    """
    images = [crop_image(screenshots[0], crop_data_dict["RATING"])]
    images.extend(crop_player_summary(screenshots[0]))
    images.extend(crop_player_specifics(screenshots[1], [[1, 3, 5, 14, 15], [13, 14, 15, 16]]))
    images.extend(crop_player_specifics(screenshots[2], [[0, 2, 6, 8, 9, 11, 12, 13, 14, 15], [10, 11, 12, 13, 14, 15, 16]]))
    images.extend(crop_player_specifics(screenshots[3], [[0, 5, 8, 13], [11, 12, 13, 14, 15, 16]]))
    images.extend(crop_player_specifics(screenshots[4], [[6], [6, 7, 9]], reverse_skip=[1, 1]))
    images.append(crop_image(screenshots[0], crop_data_dict["CARD_AREA"]))

    return images


def crop_image(img, position):
    """
    Crops an image at the given position.

    Parameters:
        img(image): source image to crop
        position(list): position to crop in the following order:
                        left, top, right, bottom

    Returns:
        cropped_img(image): image that was cropped
    """
    width, height = img.size

    left = width / position[0]
    top = height / position[1]
    right = width / position[2]
    bottom = height / position[3]

    return img.crop((left, top, right, bottom))


def crop_player_summary(img):
    """
    Crops the stats from the summary player screen. For every single stat an image is created.

    Parameters:
        img(image): image of the player performance screen

    Returns:
        images_stats(list): list of every single stat as an image
    """
    # first crop all stats in a single image
    img_stats = crop_image(img, crop_data_dict["PLAYER_SUMMARY"])

    # crop every single stat from the first image
    images_stats = []
    for i in range(17):
        images_stats.append(crop_single_stat(img_stats, i + 1, 17))

    return images_stats


def crop_player_specifics(imgs, indices_to_skip, reverse_skip=[0, 1]):
    """
    Crops the stats from a specific player screen (excluding the summary screen).
    For every single stat an image is created.

    Parameters:
        img(image): image of the player screen
        indices_to_skip(list): list of int indices to define which stats are skipped
        reverse_skip(bool): when true, indices_to_skip list defines which stats are not skipped

    Returns:
        images_stats(list): list of every single stat as an image
    """
    # first crop all stats in a single image
    img_stats = crop_image(imgs[0], crop_data_dict["PLAYER_SPECIFICS"])
    img_stats_scrolled_down = crop_image(imgs[1], crop_data_dict["PLAYER_SPECIFICS_SCROLLED_DOWN"])

    images_stats = []

    # first crop all single stats from "standard" view
    for i in range(16):
        if reverse_skip[0]:
            if i not in indices_to_skip[0]:
                continue
        else:
            if i in indices_to_skip[0]:
                continue
        images_stats.append(crop_single_stat(img_stats, i + 1, 16))

    # then crop all single stats from scrolled down view
    for i in range(17):
        if reverse_skip[1]:
            if i not in indices_to_skip[1]:
                continue
        else:
            if i in indices_to_skip[1]:
                continue
        images_stats.append(crop_single_stat(img_stats_scrolled_down, i + 1, 17))

    return images_stats


def crop_single_stat(img, pos, total_stats):
    """
    Crops a single stat at the given position.

    Parameters:
        img(image): image with all stats
        pos(int): position of the stat to crop
        total_stats(int): total number of stats in the image

    Returns:
        img_stat(image): image of the single stat
    """
    width, height = img.size

    left = 0
    top = (height / total_stats) * (pos - 1)
    right = width
    bottom = (height / total_stats) * pos

    img_stat = img.crop((left, top, right, bottom))

    return img_stat


def crop_team_data(img, home):
    """
    Crops the team data of the match facts screen from either home or away team.

    Parameters:
        img(image): image of the match facts screen
        home(bool): defines if cropping is for the home team

    Returns:
        images_stats(list): list of every single stat as an image
    """
    if home:
        img_stats = crop_image(img, crop_data_dict["HOME_DATA"])
    else:
        img_stats = crop_image(img, crop_data_dict["AWAY_DATA"])

    # crop every single stat from the first image
    images_stats = []
    for i in range(15):
        images_stats.append(crop_single_stat(img_stats, i + 1, 15))

    # crop stats from the side
    images_stats.extend(crop_team_side_data(img, home))

    return images_stats


def crop_team_side_data(img, home):
    """
    Crops the stats from the side of the match facts screen from either home or away team.

    Parameters:
        img(image): image of the match facts screen
        home(bool): defines if cropping is for home team

    Returns:
        images(list): list of every single stat as an image
    """
    if home:
        position = crop_data_dict["HOME_SIDE_DATA"]
    else:
        position = crop_data_dict["AWAY_SIDE_DATA"]

    images = []
    images.append(crop_image(img, [position[0], 3.6, position[1], 3.05]))
    images.append(crop_image(img, [position[0], 1.92, position[1], 1.77]))
    images.append(crop_image(img, [position[0], 1.32, position[1], 1.24]))

    return images