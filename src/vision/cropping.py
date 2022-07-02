import pygetwindow
import time
import pyautogui


def crop_game_data(screenshot):
    """
    Crops the game data from a screenshot taken in FIFA 22 in the match facts screen.
    Assumes the screenshot was taken in full screen and in the format 16:9.

    :param screenshot: the taken screenshot
    :return: cropped images of the game data
    """
    images = []
    images.extend(crop_team_data(screenshot, True))
    images.extend(crop_team_data(screenshot, False))

    return images


def crop_player_data(screenshot):
    """
    Crops the player data from a screenshot taken in FIFA 22 in the player performance screen.
    Assumes the screenshot was taken in full screen and in the format 16:9.

    :param screenshot: the taken screenshot
    :return: cropped images of the player data
    """
    images = [crop_rating(screenshot)]
    images.extend(crop_stats(screenshot))
    images.append(crop_card(screenshot))

    return images


def crop_rating(screenshot):
    width, height = screenshot.size

    left = width / 3.45
    top = height / 5.22
    right = width / 3.13
    bottom = height / 4.1

    img_rating = screenshot.crop((left, top, right, bottom))

    return img_rating


def crop_stats(screenshot):
    width, height = screenshot.size

    left = width / 1.12
    top = height / 3.78
    right = width / 1.08
    bottom = height / 1.14

    # first crop all stats in a single image
    img_stats = screenshot.crop((left, top, right, bottom))

    # crop every single stat from the first image
    images_stats = []
    for i in range(17):
        images_stats.append(crop_single_stat(img_stats, i + 1, 17))

    return images_stats


def crop_single_stat(img, pos, total_stats):
    width, height = img.size

    left = 0
    top = (height / total_stats) * (pos - 1)
    right = width
    bottom = (height / total_stats) * pos

    img_stat = img.crop((left, top, right, bottom))

    return img_stat


def crop_team_data(screenshot, home):
    width, height = screenshot.size

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
    img_stats = screenshot.crop((left, top, right, bottom))

    # crop every single stat from the first image
    images_stats = []
    for i in range(15):
        images_stats.append(crop_single_stat(img_stats, i + 1, 15))

    return images_stats


def crop_name(img):
    width, height = img.size

    left = width / 7.5
    top = height / 5.5
    right = width / 3.8
    bottom = height / 4

    img_cropped = img.crop((left, top, right, bottom))

    return img_cropped
    # img_cropped.save(r'C:\Users\lukas\PycharmProjects\FifaStatReader\Stats\imageName.png')


def crop_card(img):
    width, height = img.size

    left = width / 6
    top = height / 3.8
    right = width / 5.9
    bottom = height / 3.7

    img_cropped = img.crop((left, top, right, bottom))

    return img_cropped


def getImages():
    my = pygetwindow.getWindowsWithTitle('FIFA 22')[0]
    print(my)
    my.activate()
    time.sleep(1)

    screenshot = pyautogui.screenshot()
    images = [crop_name(screenshot), crop_rating(screenshot), crop_stats(screenshot)]

    return images
    # screenshot.save(r'C:\Users\lukas\PycharmProjects\FifaStatReader\Images\image.png')
