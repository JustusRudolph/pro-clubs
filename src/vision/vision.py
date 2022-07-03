import platform
import processing
from util import take_screenshot


def screenshot_fifa(wait_time):
    """
    Takes a screenshot in FIFA 22. It first opens FIFA,
    then waits the given wait_time in seconds and returns the taken screenshot.
    """
    return take_screenshot('FIFA 22', wait_time)


def process_screenshots(screenshots, names):
    """
    Takes a list of screenshots and reads the relevant data from them.
    The first screenshot must be the match facts screen. Then the player performance screens follow.
    The names of these players is given through the list names. The order of the names must
    correspond to the order of the screenshots.

    Parameters:
        screenshots(list): list of screenshots taken in FIFA 22
        names(list): list of names for the screenshots

    Returns:
        dicts(list): list of dictionaries with the full data read in the screenshots
    """
    if(platform.system() == "Windows"):
        processing.set_tesseract_path()

    dicts = []

    dicts.append(processing.get_game_data(screenshots[0]))

    for i in range(len(names)):
        dicts.append(processing.get_player_data(screenshots[i+1], names[i]))

    return dicts


# main function for testing
# if __name__ == "__main__":
#     screenshots = []
#     screenshot = screenshot_fifa()
#     # screenshot.show()
#     screenshots.append(screenshot)
#     input()
#     screenshots.append(screenshot_fifa())
#     input()
#     screenshots.append(screenshot_fifa())
# 
#     print(process_screenshots(screenshots, ["jutte", "timbo"]))