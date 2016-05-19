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
#screen.border(0)                # 0 sets the characters to default
screen.nodelay(1)               # if 1 - getch is in no-delay mode -- returns -1 if nothing is pressed

key = KEY_RIGHT                 # starting direction of the snake
score = 0

#snake = [[4,10], [4,9], [4,8]]
food = [10,20]                      # First food co-ordinates
screen.addch(food[0], food[1], '✿')    # Print the food

while key != 27:
    screen.border(0)                # let border be the default characters
    screen.addstr(0, 2, " SCORE: " + str(score) + " ")
    screen.addstr(0, 27, " SNAKE ")
    screen.timeout(150)             # speed of snake (in fact it's the screen)

    event = screen.getch()     # get the code of pressed key (if nothing pressed, this returns -1)
    if event in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
        key = event
##############################################################################
    head = [1, 1]
    body = [head[:]]*3
    deadcell = body[-1][:]
    #screen.border()
    direction = 0 #0: right, 1: down, 2: left, 3: up
    gameover = False

    while not gameover:


        if deadcell not in body:
            screen.addch(deadcell[0], deadcell[1], " ")
        screen.addch(head[0], head[1], "#")


        action = screen.getch()
        if action == curses.KEY_UP and direction != 1:
            direction = 3
        elif action == curses.KEY_DOWN and direction !=3:
            direction = 1
        elif action == curses.KEY_RIGHT and direction != 2:
            direction = 0
        elif action == curses.KEY_LEFT and direction != 0:
            direction = 2


        if direction == 0:
            head[1] += 1
        elif direction == 2:
            head[1] -= 1
        elif direction == 1:
            head[0] += 1
        elif direction == 3:
            head[0] -= 1

        deadcell = body[-1][:]
        for z in range(len(body)-1, 0, -1):                 # range(első érték, utolsó, ami nincs benne, lépték)
            body[z] = body[z-1][:]
        body[0] = head[:]


        if screen.inch(head[0], head[1]) != ord(" "):           #if snake reaches borders AND/or runs over itself
            gameover = True
            screen.move(dims[0]-1, dims[1]-1)               # move cursor to y, x position
        screen.refresh()

        time.sleep(0.1)
##############################################################################





















##############################################################################
#
# ## make snake move in direction of key pressed:
#     # if key == KEY_DOWN:
#     #     snake.insert(0, snake[0][0] + 1)
#     # elif key == KEY_UP:
#     #     snake.insert(0, snake[0][0] - 1)
#     # elif key == KEY_LEFT:
#     #     snake.insert(0, snake[0][1] - 1)
#     # elif key == KEY_RIGHT:
#     #     snake.insert(0, snake[0][1] + 1)
#     snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])
#
# # extra feature: snake crossing boundaries (comes back on the other side)
#
# ## break if snake hits wall:
#     if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59:
#         break
#
# ## break if snake runs over itself:
#     if snake[0] in snake[1:]:
#         break
##############################################################################



##############################################################################
# ## increase score if snake eats food, otherwise adjust its length:
#     if snake[0] == food:
#         food = []
#         score = score + 1               #score +=1
#         while food == []:
#             food = [randint(1, 18), randint(1, 58)]         #random coordinates of next food
#             if food in snake: food = []
#         screen.addch(food[0], food[1], "✿")
#     else:                                                  #snake decreases if
#         last = snake.pop()
#         screen.addch(last[0], last[1], " ")
#     screen.addch(snake[0][0], snake[0][1], "X")
##############################################################################


curses.endwin()
