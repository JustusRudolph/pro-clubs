import data_reader as dr
import time

# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

if __name__ == '__main__':
    start = time.time()
    print(dr.get_player_data())
    # home, away = get_game_data_dict(get_game_data())
    # print(home)
    # print(away)
    print(time.time() - start)