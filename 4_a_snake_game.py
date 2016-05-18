import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

# initializing the screen
curses.initscr()

screen = curses.newwin(20, 60, 0, 0)

curses.noecho()                 # Disable default printing of inputs
curses.curs_set(0)              # Hiding cursor visibility
screen.keypad(1)                # Mode for screen to capture key presses
curses.cbreak()                 #
screen.border(0)                # 0 sets the characters to default
screen.nodelay(1)               # if 1 - getch is in no-delay mode -- returns -1 if nothing is pressed

key = KEY_RIGHT                 # starting direction of the snake
score = 0

screen.addstr("This is a String")

snake = [[4,10]]
food = [10,20]                      # First food co-ordinates
screen.addch(food[0], food[1], '*')    # Print the food

while key != 27:
    screen.border(0)
    screen.addstr(0, 2, " SCORE: " + str(score) + " ")
    screen.addstr(0, 27, " SNAKE ")
    screen.timeout(150)             # speed of snake (in fact it's the screen)

    prevKey = key
    event = screen.getch()
    key = key if event == -1 else event

# extra feature: space bar for pausing/resuming the game

    if key not in [KEY_LEFT, KEY_UP, KEY_DOWN, KEY_RIGHT, 27]:          # if an invalid key is pressed
        key = prevKey

    if key == KEY_DOWN:
        snake.insert(0, snake[0][0] + 1)
    elif key == KEY_UP:
        snake.insert(0, snake[0][0] - 1)
    elif key == KEY_LEFT:
        snake.insert(0, snake[0][1] - 1)
    elif key == KEY_RIGHT:
        snake.insert(0, snake[0][1] + 1)

# extra feature: snake crossing boundaries (comes back on the other side)

    if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59:
        break

    if snake[0] in snake[1:]:
        break

    if snake[0] == food:
        food = []
        score = score + 1               #score +=1
        while food == []:
            food = [randint(1, 18), randint(1, 58)]         #random coordinates of next food
            if food in snake: food = []
        screen.addch(food[0], food[1], "*")
    else:                                                  #snake decreases if
        last = snake.pop()
        screen.addch(last[0], last[1], " ")
    screen.addch(snake[0][0], snake[0][1], "☕")



curses.endwin()
