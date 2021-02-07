# Heavy WIP
import curses

from utils import get_game_mode, get_game_version, get_turns, get_point_total, stub
from data import Player, Card

# Screen requirements
minimum_width = 130
minimum_height = 30

# Positions + lengths of various dynamic texts
# in the form: (y, x, length, value)
dv = {
    "turncounter": (1, 34, 3, get_turns),
    "gameversion": (1, 18, 7, get_game_version),
    "gamemode": (1, 46, 15, get_game_mode),
    "pointtotal": (1, 71, 3, get_point_total),
}

# Values for the different regions in the game
# in the form: (height, width, begin_y, begin_x)
regions = {
    "handcards": (10, 21, 4, 3),
    "userinput": (1, 17, 27, 5),
    "maincontent": (26, 50, 3, 28),
}

def init_screen(screen) -> None:

    # CURSES INIT
    curses.start_color()
    screen.keypad(True)
    screen.clear()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # /CURSES INIT



def load_interface_from_file(screen, filename: str) -> None:
    screen.clear()
    with open(filename, "r") as file:
        i = 0
        for line in file:
            screen.insstr(i, 0, line)
            i += 1

    screen.refresh()

def calibration_routine(screen) -> None:
    
    # Get size of the current window
    current_size = screen.getmaxyx()
    
    screen.resize(minimum_height, minimum_width)
    # If the sizes are adequate, return
    if current_size[0] >= minimum_height and current_size[1] >= minimum_width:
        return
    else:
        
            
        c = ""
        while c != "\n":
            screen.resize(minimum_height, minimum_width)
            load_interface_from_file(screen, "data/screens/calibration-screen.md")
            c = screen.getkey()


def display_main(screen) -> None:

    load_interface_from_file(screen, "data/screens/main-screen.md")
    screen.move(27, 5)
    

def update_hand_card(screen, p: Player) -> None:

    region = regions["handcards"]

    win = curses.newwin(region[0], region[1], region[2], region[3])

    win.clear()

    i = 0
    for line in p.get_hand_cards():
        win.addstr(i, 0, line)
        i += 1 

    win.refresh()

def update_dynamic_values(screen) -> None:

    # Go through the dictionary of all dynamic values, and overwrite their values.
    for key in dv.keys():

        # Load tuple
        obj = dv[key]

        # Get the value to print
        obj_string = str(obj[3]())

        # Right-pad the value with spaces
        obj_string = obj_string.rjust(obj[2], " ")

        # Write the value to the screen
        screen.addstr(obj[0], obj[1], obj_string, curses.color_pair(1))
    
    # Refresh the screen
    screen.refresh()
    
def retrieve_user_input(screen) -> None:
    userinput = regions["userinput"]

    # read user input (in bytes)
    rawinput = screen.getstr(userinput[2], userinput[3], userinput[1]).lower()
    
    # Decode input (using screen encoding) to a string
    res: str = rawinput.decode(screen.encoding)
    
    # Strip any underscores remaining
    res = res.rstrip("_")

    # Replace user input with underscores again
    screen.addstr(userinput[2], userinput[3], "_" * userinput[1])

    # Move cursor back to the start.
    move_cursor_to_userinput(screen)

    screen.refresh()
    return res


def move_cursor_to_userinput(screen) -> None:
    """
    Moves the cursor to where the user input starts.
    """
    userinput = regions["userinput"]
    screen.move(userinput[2], userinput[3])


def end_screen(screen) -> None:
    
    screen.keypad(False)
    curses.flushinp()
    curses.endwin()
    

def show_main_content(content: [str]) -> None:

    mc_region = regions["maincontent"]

    win = curses.newwin(mc_region[0], mc_region[1], mc_region[2], mc_region[3])
    win.clear()

    i = 0
    for line in content:
        if (i >= mc_region[0]):
            break
        win.addstr(i, 0, line)
        i += 1
    win.refresh()
