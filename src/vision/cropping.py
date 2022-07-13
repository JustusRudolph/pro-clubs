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
    images = [crop_rating(screenshots[0])]
    images.extend(crop_player_summary(screenshots[0]))
    images.extend(crop_player_specifics(screenshots[1], [1, 3, 10, 11]))
    images.extend(crop_player_specifics(screenshots[2], [0, 1, 2, 6, 7, 8]))
    images.extend(crop_player_specifics(screenshots[3], [0, 2, 5, 7, 8, 15]))
    images.extend(crop_player_specifics(screenshots[4], [9, 10], reverse_skip=True))
    images.append(crop_card(screenshots[0]))

    return images


def crop_rating(img):
    """
    Crops the rating from the image and returns the cropped image.

    Parameters:
        img(image): image of the player performance screen

    Returns:
        img_rating(image): image that only contains the rating 
    """
    width, height = img.size

    left = width / 3.45
    top = height / 5.22
    right = width / 3.13
    bottom = height / 4.1

    img_rating = img.crop((left, top, right, bottom))

    return img_rating


def crop_player_summary(img):
    """
    Crops the stats from the player performance screen. For every single stat an image is created.

    Parameters:
        img(image): image of the player performance screen

    Returns:
        images_stats(list): list of every single stat as an image
    """
    width, height = img.size

    left = width / 1.12
    top = height / 3.78
    right = width / 1.08
    bottom = height / 1.14

    # first crop all stats in a single image
    img_stats = img.crop((left, top, right, bottom))

    # crop every single stat from the first image
    images_stats = []
    for i in range(17):
        images_stats.append(crop_single_stat(img_stats, i + 1, 17))

    return images_stats


def crop_player_specifics(img, indices_to_skip, reverse_skip=False):
    width, height = img.size

    left = width / 1.09
    top = height / 3.3
    right = width / 1.04
    bottom = height / 1.14

    # first crop all stats in a single image
    img_stats = img.crop((left, top, right, bottom))

    images_stats = []
    for i in range(16):
        if reverse_skip:
            if i not in indices_to_skip:
                continue
        else:
            if i in indices_to_skip:
                continue
        images_stats.append(crop_single_stat(img_stats, i + 1, 16))

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
    width, height = img.size

    if home:
        left = width / 2.9
        top = height / 4.35
        right = width / 2.58
        bottom = height / 1.1
    else:
        left = width / 1.62
        top = height / 4.35
        right = width / 1.53
        bottom = height / 1.1

    # first crop all stats in a single image
    img_stats = img.crop((left, top, right, bottom))

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
    width, height = img.size

    if home:
        left = width / 6.4
        right = width / 4.85
    else:
        left = width / 1.27
        right = width / 1.18

    images = []

    top = height / 3.6
    bottom = height / 3.05

    images.append(img.crop((left, top, right, bottom)))

    top = height / 1.92
    bottom = height / 1.77

    images.append(img.crop((left, top, right, bottom)))

    top = height / 1.32
    bottom = height / 1.24

    images.append(img.crop((left, top, right, bottom)))

    return images


def crop_name(img):
    """
    Crops the name from the player performance screen.

    Parameters:
        img(image): iamge of the player performance screen

    Returns:
        img_name(image): image that only contains the name
    """
    width, height = img.size

    left = width / 7.5
    top = height / 5.5
    right = width / 3.8
    bottom = height / 4

    img_name = img.crop((left, top, right, bottom))

    return img_name


def crop_card(img):
    """
    Crops the area of the player performance screen where a yellow/red card would be showed.

    Parameters:
        img(image): image of the player performance screen

    Returns:
        img_card(image):  image of area where only the card is displayed
    """
    width, height = img.size

    left = width / 6
    top = height / 3.8
    right = width / 5.9
    bottom = height / 3.7

    img_card = img.crop((left, top, right, bottom))

    return img_card
