import curses
import time
import random

screen = curses.initscr()
screen.keypad(1)
dims = screen.getmaxyx()
curses.noecho()
curses.curs_set(0)

def game():
    screen.nodelay(1)
    head = [1, 1]
    body = [head[:]]*3
    screen.border()
    direction = 0 #0: right, 1: down, 2: left, 3: up
    gameover = False
    deadcell = body[-1][:]

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

game()
curses.endwin()






# def move(last_press):
#     if last_press == KEY_DOWN:
#         snake.insert(0, snake[0][0] + 1)
#     elif last_press == KEY_UP:
#         snake.insert(0, snake[0][0] - 1)
#     elif last_press == KEY_LEFT:
#         snake.insert(0, snake[0][1] - 1)
#     elif last_press == KEY_RIGHT:
#         snake.insert(0, snake[0][1] + 1)
#
# move = screen.getch()
#     if move == curses.KEY_UP and direction != 1:
#         direction = 3
#     elif move == curses.KEY_DOWN and direction !=3:
#         direction = 1
#     elif move == curses.KEY_RIGHT and direction != 2:
#         direction = 0
#     elif move == curses.KEY_LEFT and direction != 0:
#         direction = 2
#
# if direction == 0:
#     snake[0][1] += 1
# elif direction == 2:
#     snake[0][1] -= 1
# elif direction == 1:
#     snake[0][0] += 1
# elif direction == 3:
#     snake[0][0] -= 1





#snake.insert(HOVA rakjon, valamit)
#hova(0: lista elejére -- snake feje)
#mit[0:LINES][0:COLUMNS] első [0]: [4,10] -- második[0]: 4
