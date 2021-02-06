# Heavy WIP
import curses

from data.session_objects import Turn_counter, Game_mode, Game_version

# Screen requirements
minimum_width = 130
minimum_height = 30

# Positions + lengths of various dynamic texts
# in the form: (y, x, length)
dv = {
    "turncounter": (1, 34, 3, Turn_counter),
    "userinput": (27, 5, 15, ""),
    "gameversion": (1, 18, 7, Game_version),
    "gamemode": (1, 46, 15, Game_mode),
    "pointtotal": (1, 71, 3, "N/A"),
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
            load_interface_from_file(screen, "data/calibration-screen.md")
            c = screen.getkey()





def display_main(screen) -> None:

    load_interface_from_file(screen, "data/main-screen.md")
    screen.move(27, 5)
    

        

def update_dynamic_values(screen) -> None:

    # Go through the dictionary of all dynamic values, and overwrite their values.
    for key in dv.keys():

        # Load tuple
        obj = dv[key]

        # Get the value to print
        obj_string = str(obj[3])

        # Right-pad the value with spaces
        obj_string = obj_string.rjust(obj[2], " ")

        # Write the value to the screen
        screen.addstr(obj[0], obj[1], obj_string, curses.color_pair(1))
    
    # Refresh the screen
    screen.refresh()
    
    


def end_screen(screen) -> None:
    
    screen.keypad(False)
    curses.flushinp()
    curses.endwin()
    

