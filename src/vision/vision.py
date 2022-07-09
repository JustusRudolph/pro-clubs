import platform
import time
import processing
from util import take_screenshot, focus_to_window
from pynput.keyboard import Controller


def screenshot_fifa(wait_time=1, player=True):
    """
    Takes one or more screenshots in FIFA 22, depending on the player variable.
    It first opens FIFA, then waits the given wait_time in seconds and returns the taken screenshots.

    Parameters:
        wait_time(float): wait time after application was opened and first screenshot is taken
        player(bool): defines if the screenshot is taken in the match or player screen

    Returns:
        screenshots: single screenshot when match screen, multiple screenshots as list when player screen
    """
    keyboard = Controller()

    focus_to_window('FIFA 22')
    time.sleep(wait_time)

    if not player:
        return take_screenshot(0)

    screenshots = []

    for i in range(5):
        screenshots.append(take_screenshot(0.5))
        keyboard.press('c')
        time.sleep(0.1)
        keyboard.release('c')

    return screenshots
    

def process_screenshots(screenshots, names, path='C:\\Program Files\\Tesseract-OCR\\tesseract'):
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
        processing.set_tesseract_path(path)

    dicts = []

    dicts.append(processing.get_game_data(screenshots[0]))

    for i in range(len(names)):
        dicts.append(processing.get_player_data(screenshots[i+1], names[i]))

    return dicts


# main function for testing
if __name__ == "__main__":
    processing.set_tesseract_path('C:\\Program Files\\Tesseract-OCR\\tesseract')
    screenshots = []
    screenshots.append(screenshot_fifa(player=False))
    input("taken first")
    screenshots.append(screenshot_fifa())
    input("taken second")
    start = time.time()
    print(len(processing.get_player_data(screenshots[1])))
    print("time: " + str(time.time() - start))