import platform
import time
import processing
from util import take_screenshot, focus_to_window
from pynput.keyboard import Controller


def screenshot_fifa(wait_time=1, player=True, name=""):
    """
    Takes one or more screenshots in FIFA 22, depending on the player variable.
    It first opens FIFA, then waits the given wait time in seconds and returns the taken screenshots.

    Parameters:
        wait_time(float): wait time after application was opened and first screenshot is taken
        player(bool): defines if the screenshot is taken in the match or player screen
        name(string): name of the player, only relevant when taken in player screen

    Returns:
        screenshots: single screenshot when match screen,
                     dictionary with name and screenshots when player screen
    """
    keyboard = Controller()

    focus_to_window('FIFA 22')
    time.sleep(wait_time)

    if not player:
        return take_screenshot(0)

    dict = {"NAME": name}
    screenshots = []

    for i in range(5):
        screenshots.append(take_screenshot(0.5))
        keyboard.press('c')
        time.sleep(0.1)
        keyboard.release('c')

    dict["SCREENSHOTS"] = screenshots

    return dict
    

def process_screenshots(data, path='C:\\Program Files\\Tesseract-OCR\\tesseract'):
    """
    Takes a list of screenshots and reads the relevant data from them.
    The first screenshot must be from the match facts screen. Then the player screens follow,
    for each player a separate list. The names of the players is given through the list names.
    The order of the names must correspond to the order of the screenshots of the players.

    Parameters:
        screenshots(list): list of screenshots taken in FIFA 22
        names(list): list of names for the screenshots

    Returns:
        dicts(list): list of dictionaries with the full data read in the screenshots
    """
    if(platform.system() == "Windows"):
        processing.set_tesseract_path(path)

    game_dict = processing.get_game_data(data[0])

    player_dicts = []

    for i in range(len(data)-1):
        player_dicts.append(processing.get_player_data(data[i+1]["SCREENSHOTS"], data[i+1]["NAME"]))

    return [game_dict, player_dicts]


# main function for testing
# if __name__ == "__main__":
#     # processing.set_tesseract_path('C:\\Program Files\\Tesseract-OCR\\tesseract')
#     screenshots = []
#     screenshots.append(screenshot_fifa(player=False))
#     input("taken first")
#     screenshots.append(screenshot_fifa(name="Timbo"))
#     input("taken second")
#     screenshots.append(screenshot_fifa(name="Jutte"))
#     start = time.time()
#     print(process_screenshots(screenshots))
#     print("time: " + str(time.time() - start))