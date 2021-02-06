# Heavy WIP
import curses


# Screen requirements
minimum_width = 130
minimum_height = 30

# Positions + lengths of various dynamic texts
# in the form: (y, x, length)
turncounter_text = (1, 34, 3)
userinput_curserpos = (27, 5, 15)
gameversion_text = (1, 18, 7)
gamemode_name_text = (1, 46, 15)
point_total_text = (1, 71, 3)

# CURSES INIT
screen = curses.initscr()
curses.start_color()
screen.keypad(True)
screen.clear()

curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
# /CURSES INIT

screen.resize(minimum_height, minimum_width)


def display_borders(screen) -> None:

    with open("mockup.md", "r") as file:
        i = 0
        for line in file:
            screen.insstr(i, 0, line)
            i += 1
    screen.refresh()
# Wait for some input

display_borders(screen)
screen.move(27, 5)

c = ""
while c != "q":
    c = screen.getkey()


# CURSES END
screen.keypad(False)
curses.beep()
curses.flushinp()
curses.endwin()
# /CURSES END