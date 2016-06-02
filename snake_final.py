import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import time


def init_screen():
    global screen, key, life
    curses.initscr()
    curses.noecho()                 # Disable default printing of inputs
    curses.curs_set(0)              # Hiding cursor visibility
    curses.cbreak()                 # No need to press enter after key press

    if curses.has_colors():
        curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    screen = curses.newwin(20, 60, 0, 0)
    screen.keypad(1)                # Mode for screen to capture key presses
    screen.border(0)                # 0 sets the characters to default
    screen.nodelay(1)               # if 1 - getch is in no-delay mode -- returns -1 if nothing is pressed

    key = KEY_RIGHT                 # starting direction of the snake
    life = 3

    screen.timeout(150)             # speed of snake (in fact it's the screen)


def game():
    global screen, score, food, direction, head, body, gameover, tail, life
    food_char = '✿'
    heart_char = '💓'
    bkgd_char = ' '

    allowed_chars = [ord(food_char), ord(heart_char), ord(bkgd_char)]

    screen.clear()
    screen.border(0)                # let border be the default characters
    score = 0

    food = [randint(1, 18), randint(1, 58)]                      # First food co-ordinates
    screen.addch(food[0], food[1], food_char, curses.color_pair(3))    # Print the food

    heart = [randint(1, 18), randint(1, 58)]                      # First food co-ordinates
    screen.addch(heart[0], heart[1], heart_char, curses.color_pair(3))

    poison = [randint(1, 13), randint(1, 58)]                    # First poison co-ordinates
    # for i in range(5):
    #     screen.addch(poison[0], poison[1] + i, "▊", curses.color_pair(3))
        # screen.addch(poison[0], poison[1], 'x', curses.color_pair(3))

    head = [9, 25]
    body = [head[:]]*3
    direction = 0  # 0: right, 1: down, 2: left, 3: up
    gameover = False
    tail = body[-1][:]

    while not gameover:

        dir_move()

        if screen.inch(head[0], head[1]) not in allowed_chars:
        # if screen.inch(head[0], head[1]) == ord("x") and head[0] == 0 and head [0] == 19 and head[1] == 0 and head[1] == 59:
        # if snake reaches borders AND/or runs over itself
            gameover = True
            life -= 1


        screen.border(0)
        screen.addstr(0, 2, " SCORE: " + str(score) + " ")
        screen.addstr(0, 49, " LIFE: " + str(life) + " ")
        screen.addstr(0, 27, " SNAKE ")

        # add life (heart consumption)
        if head == heart:
            life += 1
            heart = [randint(1, 18), randint(1, 58)]
            screen.addstr(heart[0], heart[1], heart_char, curses.color_pair(3))
            body += [head[:]]

        # food consumption
        if head == food:
            score += 1
            food = [randint(1, 18), randint(1, 58)]
            screen.addstr(food[0], food[1], food_char, curses.color_pair(3))
            body += [head[:]]

        if (score + 1) % 5 == 0:
            # poison = [randint(1, 13), randint(1, 58)]
            for i in range(5):
                screen.addch(poison[0], poison[1] + i, "▊", curses.color_pair(3))



        screen.refresh()

        time.sleep(0.005)


def dir_move():
    global direction, tail, gameover, life

    # draw the snake
    if tail not in body:
        screen.addch(tail[0], tail[1], " ")
    screen.addstr(head[0], head[1], "o", curses.color_pair(1))

    # defining directions
    key_press = screen.getch()
    if key_press == curses.KEY_UP and direction != 1:
        direction = 3
    elif key_press == curses.KEY_DOWN and direction != 3:
        direction = 1
    elif key_press == curses.KEY_RIGHT and direction != 2:
        direction = 0
    elif key_press == curses.KEY_LEFT and direction != 0:
        direction = 2
    elif key_press == ord("q"):
        life = -1
        gameover = True

    # head moves 1 step further
    if direction == 0:
        head[1] += 1
    elif direction == 2:
        head[1] -= 1
    elif direction == 1:
        head[0] += 1
    elif direction == 3:
        head[0] -= 1

    # tail catches up with body
    tail = body[-1][:]

    # body moves forward, catches up with head, leaves tail behind
    for z in range(len(body)-1, 0, -1):
        body[z] = body[z-1][:]
    body[0] = head[:]


def gameover_screen():
    screen.clear()
    screen.border(0)
    screen.addstr(8, 25, "GAME OVER")
    screen.getch()
    time.sleep(5)


def start_screen():
    screen.clear()
    screen.border(0)
    screen.addstr(8, 25, "Hello")
    screen.addstr(19, 16, " Press any key to start ")
    start_key = screen.getch()
    while start_key < 0:
        start_key = screen.getch()

init_screen()
start_screen()
while life > 0:
    game()
gameover_screen()
curses.endwin()
