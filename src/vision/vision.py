import platform, time
from pynput.keyboard import Controller

from vision import processing, util


def screenshot_fifa(wait_time=1, player=True):
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

    util.focus_to_window('FIFA 22')
    time.sleep(wait_time)

    if not player:
        return util.take_screenshot(0)

    screenshots = []

    for i in range(5):
        screenshots.append(util.take_screenshot(0.5))
        keyboard.press('c')
        time.sleep(0.1)
        keyboard.release('c')

    return screenshots
    

def process_screenshots(screenshots, path='C:\\Program Files\\Tesseract-OCR\\tesseract'):
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

    game_dict = processing.get_game_data(screenshots[0])

    player_dicts = []

    for key in screenshots[1]:
        player_dicts.append(processing.get_player_data(screenshots[1][key], key))

    return [game_dict, player_dicts]


# main function for testing
if __name__ == "__main__":
    # processing.set_tesseract_path('C:\\Program Files\\Tesseract-OCR\\tesseract')
    screenshots = [0, {}]
    screenshots[0] = screenshot_fifa(player=False)
    input("taken first")
    screenshots[1]["Timbo"] =  (screenshot_fifa())
    input("taken second")
    screenshots[1]["Jutte"] =  (screenshot_fifa())
    start = time.time()
    print(process_screenshots(screenshots))
    print("time: " + str(time.time() - start))