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
        'SPACE': ord(chr(32)),
        'CTRL+E': ord(chr(5)),
        'CTRL+N': ord(chr(14))
    }

    for i in range(ord('a'), ord('z')):
        char_map[chr(i)] = i

    init_curses()
    curses.init_pair(1, 215,  -1)  # orange
    curses.init_pair(2, 255, -1)   # white
    curses.init_pair(3, 245, -1)   # grey
    curses.init_pair(4, 197, -1)   # red
    curses.init_pair(5, 47, -1)    # green

    rand_select = random.choice(list(char_map))
    curr_char = 0
    history_prefix = 'History: '
    history_prefix_len = len(history_prefix)
    history = []

    while True:
        screen.addstr(0, 0, 'Press Ctrl+C to quit.', curses.color_pair(1))
        screen.addstr(1, 0, 'Type {0}'.format(rand_select).encode('utf_8'), curses.color_pair(2))
        screen.addstr(2, 0, 'Pressed: {0}:{1}'.format(curr_char, chr(curr_char)).encode('utf_8'))
        screen.addstr(3, 0, history_prefix, curses.color_pair(3))

        for ix, record in enumerate(reversed(history[-10:])):
            screen.addstr(
                3,
                history_prefix_len + ix,
                '{0}'.format(record['entry']),
                curses.color_pair(record['color'])
            )

        curr_char = screen.getch()

        entry_color = 5
        if (rand_select in char_map and char_map[rand_select] == curr_char):
            rand_select = random.choice(list(char_map))
        else:
            entry_color = 4
            sys.stdout.flush()
        history.append({'entry': chr(curr_char), 'color': entry_color})

        screen.clear()

    destroy_curses()
    exit(0)


if __name__ == "__main__":
    try:
        main()
    except:
        destroy_curses()
