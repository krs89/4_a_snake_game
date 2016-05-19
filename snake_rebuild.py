import curses
import time
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from curses import wrapper

def main(scr):
    win = curses.newwin(curses.LINES, curses.COLS, 0, 0)  # Init window object
    #curses.noecho()             # Disable default printing of inputs
    #win.keypad(1)               # enable processing of functional keys by curses (ex. arrow keys)
    curses.curs_set(0)          # Hiding cursor visibility (https://docs.python.org/2/library/curses.html#curses.curs_set)

    win.border(0)               # set a border for the window
    win.nodelay(1)

    title = ' Hello snake! '
    win.addstr(0, (curses.COLS - len(title)) // 2, title)

# initialize values:
    head = [1, 1]
    body = [head[:]]*3
    direction = 0 #0: right, 1: down, 2: left, 3: up
    gameover = False
    deadcell = body[-1][:]
    key_press = curses.KEY_RIGHT

    while key_press != 27:            # not Esc is pressed
        win.timeout(100)        # wait 0.1 sec

    # get key presses and directions
        key_press = win.getch()
        if key_press == curses.KEY_UP and direction != 1:
            direction = 3
        elif key_press == curses.KEY_DOWN and direction !=3:
            direction = 1
        elif key_press == curses.KEY_RIGHT and direction != 2:
            direction = 0
        elif key_press == curses.KEY_LEFT and direction != 0:
            direction = 2


    # make it move in direction
        if direction == 0:
            head[1] += 1
        elif direction == 2:
            head[1] -= 1
        elif direction == 1:
            head[0] += 1
        elif direction == 3:
            head[0] -= 1

        deadcell = body[-1][:]
        for z in range(len(body)-1, 0, -1):
            body[z] = body[z-1][:]
        body[0] = head[:]
    # food








        #win.addch(last[0], last[1], ' ')            # clear last character of the snake

        #win.addch(head[0][0], head[0][1], 'x')    # add a new character where the snake moved
        win.refresh()

    game_over = 'Game Over!'
    win.addstr(curses.LINES // 2, (curses.COLS - len(game_over)) // 2, game_over)
    win.refresh()

    time.sleep(3)       # wait to show the Game Over text for 3 secs

curses.wrapper(main)    # use curses wrapper
# wrapper() turns on cbreak mode, turns off echo, enables the terminal keypad, and initializes colors
