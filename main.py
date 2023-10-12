import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()

    # Get terminal dimensions
    term_height, term_width = stdscr.getmaxyx()

    welcome_text = "Welcome to the Speed Typing Test!"
    press_key_text = "Press any key to begin!"

    # Calculate the positions to center the text horizontally
    welcome_text_x = (term_width - len(welcome_text)) // 2
    press_key_text_x = (term_width - len(press_key_text)) // 2

    # Calculate the positions to center the text vertically
    welcome_text_y = term_height // 2 - 1
    press_key_text_y = term_height // 2

    # Add the centered text to the screen
    stdscr.addstr(welcome_text_y, welcome_text_x, welcome_text)
    stdscr.addstr(press_key_text_y, press_key_text_x, press_key_text)
    
    stdscr.refresh()
    stdscr.getkey()

target_text_x = 0
wpm_text_y = 0

def display_text(stdscr, target, current, wpm=0):
    term_height, term_width = stdscr.getmaxyx()
    
    #Calculate the positions to center the text horizontally
    global target_text_x 
    target_text_x = (term_width - len(target)) // 2

    #Calculate the positions to center the text vertically
    target_text_y = term_height // 2-1
    global wpm_text_y 
    wpm_text_y = term_height // 2
    
    stdscr.addstr(target_text_y, target_text_x, target)
    stdscr.addstr(wpm_text_y,target_text_x,f"WPM: {wpm}")

    for i, char in enumerate(current): #loops through and gives index and char
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(target_text_y, i+target_text_x, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()  #strip removes the \n on the string


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed/60)) / 5)
        
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        elif ord(key) == 9:
            stdscr.refresh()
            stdscr.clear()
            wpm_test(stdscr)
            break  


        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif (len(current_text) < len(target_text)) and ((ord(key) <=122 and ord(key)>=97) or ord(key)==32 or ord(key)==44 or ord(key)==39 or ord(key)==45):
                current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #sets text color green with white background
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) #sets text color yellow with white background
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) 

    #global variables x,y coordinates for the finished_text output
    target_text_x
    wpm_text_y

    finished_text = "You completed the text! Press any key to continue or ESC to quit..."

    term_height, term_width = stdscr.getmaxyx()
    
    #Calculate the position to center the text horizontally
    finished_text_x = (term_width - len(finished_text)) // 2

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(wpm_text_y+2, finished_text_x, finished_text)
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)

