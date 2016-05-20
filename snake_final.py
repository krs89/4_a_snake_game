import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import time



def init_screen():
    global screen, score, food, key
    curses.initscr()

    if curses.has_colors():
        curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)


    screen = curses.newwin(20, 60, 0, 0)

    curses.noecho()                 # Disable default printing of inputs
    curses.curs_set(0)              # Hiding cursor visibility
    screen.keypad(1)                # Mode for screen to capture key presses
    curses.cbreak()                 #
    screen.border(0)                # 0 sets the characters to default
    screen.nodelay(1)               # if 1 - getch is in no-delay mode -- returns -1 if nothing is pressed

    key = KEY_RIGHT                 # starting direction of the snake
    score = 0
    food = [randint(1, 18), randint(1, 58)]                      # First food co-ordinates
    screen.addch(food[0], food[1], '✿', curses.color_pair(3))    # Print the food

    screen.border(0)                # let border be the default characters
    screen.addstr(0, 27, " SNAKE ")
    screen.timeout(150)             # speed of snake (in fact it's the screen)

def game():
    global screen, score, food, direction, head, body, gameover, tail

    #exit = -1
    head = [9, 25]
    body = [head[:]]*3
    direction = 0                           #0: right, 1: down, 2: left, 3: up
    gameover = False
    tail = body[-1][:]


    while not gameover: #and q < 0:
        #screen.bkgd(" ", curses.color_pair(2))

        #exit = screen.getch()                      # press q to exit


        dir_move()


        if screen.inch(head[0], head[1]) != ord(" ") and screen.inch(head[0], head[1]) != ord("✿"): #or exit == 27:           #if snake reaches borders AND/or runs over itself
            gameover = True

        screen.addstr(0, 2, " SCORE: " + str(score) + " ")

## food consumption
        if head == food:
            score = score + 1
            food = [randint(1, 18), randint(1, 58)]
            screen.addstr(food[0], food[1], '✿', curses.color_pair(3))
            body += [head[:]]
        else:
            pass


        screen.refresh()

        time.sleep(0.005)

def dir_move():
    global direction, tail

    if tail not in body:
        screen.addch(tail[0], tail[1], " ")
    screen.addstr(head[0], head[1], " ", curses.color_pair(1))

## defining directions
    key_press = screen.getch()
    if key_press == curses.KEY_UP and direction != 1:
        direction = 3
    elif key_press == curses.KEY_DOWN and direction !=3:
        direction = 1
    elif key_press == curses.KEY_RIGHT and direction != 2:
        direction = 0
    elif key_press == curses.KEY_LEFT and direction != 0:
        direction = 2


    if direction == 0:
        head[1] += 1
    elif direction == 2:
        head[1] -= 1
    elif direction == 1:
        head[0] += 1
    elif direction == 3:
        head[0] -= 1

## making the snake move
    tail = body[-1][:]
    for z in range(len(body)-1, 0, -1):
        body[z] = body[z-1][:]
    body[0] = head[:]


init_screen()
game()

curses.endwin()
