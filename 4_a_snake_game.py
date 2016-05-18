import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

screen = curses.initscr()
curses.noecho()                 # Disable default printing of inputs
curses.curs_set(0)              # Hiding cursor visibility
screen.keypad(1)                # Mode for screen to capture key presses

screen.addstr("This is a String")

food = [10,20]                      # First food co-ordinates
screen.addch(food[0], food[1], '*')    # Print the food

while True:
   event = screen.getch()
   if event == ord("q"): break
   elif event == curses.KEY_UP:
      screen.clear()
      screen.addstr("The User Pressed UP")
   elif event == curses.KEY_DOWN:
      screen.clear()
      screen.addstr("The User Pressed DOWN")

curses.endwin()
