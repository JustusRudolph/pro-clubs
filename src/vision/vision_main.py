import platform, time, pyautogui
import pynput.keyboard as keyboard, pynput.mouse as mouse
from . import processing, util

CURRENT_PLATFORM = platform.system()


def screenshot_fifa(player=True, current_fifa='FIFA 23', wait_time=0.3):
    """
    Takes one or more screenshots in FIFA 22, depending on the player variable.
    It first opens FIFA, then waits the given wait time in seconds and returns the taken screenshots.

    Parameters:
        player(bool): defines if the screenshot is taken in the match or player screen
        current_fifa(string): current name/version of fifa to take screenshots from
        wait_time(float): wait time after application was opened and first screenshot is taken

    Returns:
        screenshots: single screenshot when match screen,
                     list of screenshots when player screen
    """
    mouse_controller = mouse.Controller()

    if(CURRENT_PLATFORM == "Windows"): # focus to window only works on windows for now
        util.focus_to_window(current_fifa)

    time.sleep(wait_time)

    if not player:
        return util.take_screenshot(0.3)

    screenshots = []

    for i in range(5):
        sc1 = util.take_screenshot(0.3)
        if i == 0: # for the summary screen one screenshot is enough
            screenshots.append(sc1)
            util.keyboard_press('c')
            continue

        # for the other screens we need to scroll down to see all data
        mouse_controller.position = (3640, 640)
        util.mouse_move_down_while_pressed(mouse.Button.left, 500)
        
        sc2 = util.take_screenshot(0.3)
        screenshots.append([sc1, sc2])
        util.keyboard_press('c')

    # press c once more to return to default view
    time.sleep(0.1)
    util.keyboard_press('c')

    return screenshots


def screenshot_fifa_22(wait_time=1, player=True):
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
    keyboard = keyboard.Controller()

    if(CURRENT_PLATFORM == "Windows"): # focus to window only works on windows for now
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

    time.sleep(0.1)
    keyboard.press('c')
    time.sleep(0.1)
    keyboard.release('c')

    return screenshots


def process_screenshots(screenshots, path='C:\\Program Files\\Tesseract-OCR\\tesseract'):
    """
    Takes a list of screenshots and reads the relevant data from them.
    The first screenshot must be from the match facts screen. Then a list of dicts
    follows, the keys being the player name and the value the list of screenshots.
    Returns a list of dictionaries with the data and list with misread data.

    Parameters:
        screenshots(list): list of screenshots taken in FIFA 22

    Returns:
        dicts(list): list of dictionaries with the full data read in the screenshots
        misreads(list): list of tuples, the second value is the attribute that was read wrong,
                        the first value either the name of the player or 0/1 for home/away team
    """
    if(CURRENT_PLATFORM == "Windows"):
        processing.set_tesseract_path(path)

    game_dict, misreads = processing.get_game_data(screenshots[0])

    player_dicts = []

    for key in screenshots[1]:
        player_dict, player_misreads = processing.get_player_data(screenshots[1][key], key)
        player_dicts.append(player_dict)
        misreads.extend(player_misreads)

    return [game_dict, player_dicts], misreads
    