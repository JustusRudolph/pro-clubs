import time

import processing, util

if __name__ == '__main__':
    start = time.time()
    for i in range(1):
        # player_dict = processing.get_player_data(util.take_screenshot('FIFA 22', 1), "test")
        # print(player_dict)
        game_dict = processing.get_game_data(util.take_screenshot('FIFA 22', 1))
        print(game_dict)
    print(time.time() - start)
