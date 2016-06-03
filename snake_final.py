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

    # defining colours
    if curses.has_colors():
        curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)

    screen = curses.newwin(20, 60, 0, 0)
    screen.keypad(1)                # Mode for screen to capture key presses
    screen.border(0)                # 0 sets the characters to default
    screen.nodelay(1)               # if 1 - getch is in no-delay mode -- returns -1 if nothing is pressed

    key = KEY_RIGHT                 # starting direction of the snake
    life = 3

def random_position(good_place):
    random_pos = [randint(1, 18), randint(1, 58)]
    while screen.inch(random_pos[0], random_pos[1]) != good_place:
        random_pos = [randint(1, 18), randint(1, 58)]
        break
    return random_pos

def game():
    global screen, score, food, direction, head, body, gameover, tail, life

    # defining characters
    food_char = '✿'
    heart_char = '♥'
    bkgd_char = ' '
    wall_char = "▊"

    # characters the snake can touch without dying
    allowed_chars = [ord(food_char), ord(heart_char), ord(bkgd_char)]

    # setting up the screen
    screen.clear()
    screen.border(0)
    score = 0


    food = random_position(bkgd_char)                      # First food co-ordinates
    screen.addch(food[0], food[1], food_char, curses.color_pair(3))    # Print the food

    heart = random_position(bkgd_char)                      # First heart co-ordinates

    poison = []                    # creating a list for the future "poison" (wall)

    # starting position of the snake
    head = [9, 25]
    body = [head[:]]*3
    tail = body[-1][:]
    direction = 0  # 0: right, 1: down, 2: left, 3: up
    gameover = False

    while not gameover:

        # snake's direction and movement
        dir_move()

        # snake dies if it reaches the borders, runs over itself or touches the wall ("poison")
        if screen.inch(head[0], head[1]) not in allowed_chars:
            gameover = True
            life -= 1

        screen.border(0)
        screen.addstr(0, 2, " SCORE: " + str(score) + " ")
        screen.addstr(0, 49, " LIFE: " + str(life) + " ")
        screen.addstr(0, 27, " SNAKE ")

        old_score = score

        if head == heart:
            life += 1
            score += 1
            body += [head[:]]

        # food consumption
        if head == food:
            score += 1
            food = random_position(bkgd_char)
            screen.addstr(food[0], food[1], food_char, curses.color_pair(3))
            body += [head[:]]

        # add life (heart consumption)
        if (score + 1) % 4 == 0 and old_score != score:
            heart = random_position(bkgd_char)
            screen.addch(heart[0], heart[1], heart_char, curses.color_pair(2))

        # "poison" aka wall
        if (score + 1) % 3 == 0 and old_score != score:
            poison_head = [randint(1, 13), randint(1, 53)]
            VERT = 1
            HOR = 2
            DIAG_R = 3
            DIAG_L = 4
            pos = randint(1, 5)  # position of the wall
            for i in range(5):  # length of wall
                if pos == 1:
                    poison.append((poison_head[0] + i, poison_head[1]))
                    screen.addch(poison_head[0] + i, poison_head[1], wall_char, curses.color_pair(3))
                elif pos == 2:
                    poison.append((poison_head[0], poison_head[1] + i))
                    screen.addch(poison_head[0], poison_head[1] + i, wall_char, curses.color_pair(3))
                elif pos == 3:
                    poison.append((poison_head[0] + i, poison_head[1] + i))
                    screen.addch(poison_head[0] + i, poison_head[1] + i, wall_char, curses.color_pair(3))
                elif pos == 4:
                    poison.append((poison_head[0] + i, poison_head[1] - i))
                    screen.addch(poison_head[0] + i, poison_head[1] - i, wall_char, curses.color_pair(3))

        screen.refresh()
        screen.timeout(150)
        # speeding up the snake
        if score > 5:
            screen.timeout(75)
        elif score > 10:
            screen.timeout(50)


def dir_move():
    global direction, tail, gameover, life

    # drawing the snake
    if tail not in body:
        screen.addch(tail[0], tail[1], " ")
    screen.addstr(head[0], head[1], " ", curses.color_pair(1))

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
    # screen.bkgd(' ', curses.color_pair(4))
    screen.addstr(8, 25, "GAME OVER")
    screen.getch()
    time.sleep(2)


def start_screen():
    screen.clear()
    screen.border(0)
    screen.addstr(8, 25, "HELLO!")
    screen.addstr(19, 17, " Press any key to start ")
    start_key = screen.getch()
    while start_key < 0:
        start_key = screen.getch()

init_screen()
start_screen()
while life > 0:
    game()
gameover_screen()
curses.endwin()
