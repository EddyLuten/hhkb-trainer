#!/usr/bin/env python3
import sys
import random
import signal
import curses

screen = 0

def destroy_curses():
    global screen
    curses.curs_set(1)
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

def init_curses():
    global screen
    screen = curses.initscr()
    screen.keypad(1)
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()

def signal_handler(signal,  frame):
    destroy_curses()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT,  signal_handler)

    char_map = {
        u'\u2190': curses.KEY_LEFT,
        u'\u2191': curses.KEY_UP,
        u'\u2192': curses.KEY_RIGHT,
        u'\u2193': curses.KEY_DOWN,
        'PGDN': curses.KEY_NPAGE,
        'PGUP': curses.KEY_PPAGE,
        'DEL': curses.KEY_DC,
        'END': curses.KEY_END,
        'BACKSPACE': ord(chr(127)),
        'HOME': curses.KEY_HOME,
        'TAB': ord(chr(9)),
        'RETURN': ord(chr(10)),
        'SPACE': ord(chr(32))
    }

    for i in range(ord('a'), ord('z')):
        char_map[chr(i)] = i

    init_curses()
    curses.init_pair(1, 125,  -1)
    curses.init_pair(2, 255, -1)
    curses.init_pair(3, 238, -1)

    rand_select = random.choice(list(char_map))
    curr_char = 0
    history = ''

    while True:
        screen.addstr(0, 0, 'Press Ctrl+C to quit.', curses.color_pair(1))
        screen.addstr(1, 0, 'Type {0}'.format(rand_select).encode('utf_8'), curses.color_pair(2));
        screen.addstr(2, 0, 'Pressed: {0}:{1}'.format(curr_char, chr(curr_char)).encode('utf_8'))
        screen.addstr(3, 0, 'History: {0}'.format(history), curses.color_pair(3))

        curr_char = screen.getch()
        history = (chr(curr_char) if 32 <= curr_char <= 126 else ' ') + history

        if  (rand_select in char_map and char_map[rand_select] == curr_char):
            rand_select = random.choice(list(char_map))
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()

        history = history if len(history) < 10 else history[:10]
        screen.clear()

    destroy_curses()
    exit(0)

if __name__ == "__main__":
    main()
