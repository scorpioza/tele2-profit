import time
from colorama import init as colorama_init, Fore

from config import PRINT_TO_LOG, LOG_PATH

def xprint(color, msg, show_time=False):
    print(color+msg)
    if(show_time):
        msg = "--------------------------\nTIME: "+time.strftime('%Y-%m-%d %H:%M:%S')+"\n"+msg
    if PRINT_TO_LOG:
        f = open(LOG_PATH, "a")
        f.write(msg+"\n\n")
        f.close()