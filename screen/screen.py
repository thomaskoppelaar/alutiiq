# Heavy WIP
import curses

from utils import get_game_mode, get_game_version, get_turns, get_point_total, stub
from data import Player, Card
from screen.regions import Region, turncounter, gameversion, gamemode, pointtotal
from screen.regions import handcards, userinput, maincontent
from data.session_objects import Turn_counter, Game_mode, Game_version


# Screen requirements
minimum_width = 130
minimum_height = 30

class Screen:

    screen = None
    mcwin = None
    hcwin = None

    mc_content: [str] = []
    mc_linepos: int = 0
    

    def __init__(self):
        self.screen = curses.initscr()




    def init_screen(self) -> None:

        # CURSES INIT
        curses.start_color()
        self.screen.keypad(True)
        self.screen.clear()

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # /CURSES INIT



    def load_interface_from_file(self, filename: str) -> None:
        
        self.screen.clear()
        with open(filename, "r") as file:
            i = 0
            for line in file:
                self.screen.insstr(i, 0, line)
                i += 1

        self.screen.refresh()

    def calibration_routine(self) -> None:
        
        # Get size of the current window
        current_size = self.screen.getmaxyx()
        
        self.screen.resize(minimum_height, minimum_width)
        # If the sizes are adequate, return
        if current_size[0] >= minimum_height and current_size[1] >= minimum_width:
            return
        else:
            
                
            c = ""
            while c != "\n":
                self.screen.resize(minimum_height, minimum_width)
                self.load_interface_from_file("data/screens/calibration-screen.md")
                c = self.screen.getkey()


    def display_main(self) -> None:

        self.load_interface_from_file("data/screens/main-screen.md")

        self.screen.addstr(gamemode.y, gamemode.x, Game_mode.rjust(gamemode.width, " "))
        self.screen.addstr(gameversion.y, gameversion.x, Game_version.rjust(gameversion.width, " "))

        self.screen.move(27, 5)
    

    def update_hand_card(self, p: Player) -> None:


        self.hcwin = curses.newwin(handcards.height, handcards.width, handcards.y, handcards.x)

        self.hcwin.clear()

        i = 0
        for line in p.get_hand_cards():
            self.hcwin.addstr(i, 0, line)
            i += 1 

        self.hcwin.refresh()

    def update_dynamic_values(self, p: Player) -> None:

        self.screen.addstr(turncounter.y, turncounter.x, str(Turn_counter).rjust(turncounter.width, " "))
        self.screen.addstr(pointtotal.y, pointtotal.x, str(p.get_hand_value()).rjust(pointtotal.width, " "))

        
        # Refresh the screen
        self.screen.refresh()
    
    def retrieve_user_input(self) -> None:
        """
        Method that allows the user to input text, whilst also allowing the user to scroll the main content.

        """

        self.move_cursor_to_userinput()

        index: int  = 0
        res: [str] = []

        # Get input character
        c = self.screen.getch()

        # 10 is the code for \n, aka newline, aka enter
        while c != 10:

            # Scroll the main content up or down
            if c == curses.KEY_DOWN:
                self.scroll_down()
            elif c == curses.KEY_UP:
                self.scroll_up()

            # Moving the cursor using left/right keys
            elif c == curses.KEY_LEFT:

                # Make sure we don't leave the designated space
                index = max(0, index - 1)

                # Move the cursor accordingly
                self.screen.move(userinput.y, userinput.x + index)

            elif c == curses.KEY_RIGHT:

                # Make sure we don't leave the designated space
                index = min(userinput.width - 1, index + 1)

                # Move the cursor accordingly
                self.screen.move(userinput.y, userinput.x + index)


            # Backspace key:
            elif c == 127:

                # Try deleting the character.
                # If said character does not exist, pass
                try:
                    res.pop(index-1)
                    index = max(0, index - 1)

                except IndexError:
                    pass
            else:

                # Catch any ValueError, that gets thrown
                # if any character is sent that isn't ASCII.
                # Mainly in place as a failsafe.
                try:

                    # Save the character at the correct place
                    if len(res) >= userinput.width:
                        res[index] = chr(c)
                    else:
                        res.insert(index, chr(c))

                    # Get the new index
                    index = min(userinput.width - 1, index + 1)
                
                except ValueError:
                    pass


            # Print new string
            self.screen.addstr(userinput.y, userinput.x, "".join(res).ljust(userinput.width, "_"))

            # Move cursor back to index, as addstr moves it
            self.screen.move(userinput.y, userinput.x + index)
            
            # Refresh
            self.screen.refresh()
                
            # Wait for new character
            c = self.screen.getch()
        
        # Replace user input with underscores again
        self.screen.addstr(userinput.y, userinput.x, "_" * userinput.width)

        # Move cursor back to the start.
        self.move_cursor_to_userinput()

        self.screen.refresh()

        return "".join(res)

    def scroll_up(self) -> None:
        if self.mcwin is None: return

        mc: Region = maincontent

        # Don't scroll more than is needed
        self.mc_linepos = max(self.mc_linepos - 1, 0)

        # Refresh the main content pad, start showing content from the new starting line.
        self.mcwin.refresh(self.mc_linepos, 0, mc.y, mc.x, mc.y + mc.height, mc.x + mc.width)

    def scroll_down(self) -> None:
        if self.mcwin is None: return

        mc: Region = maincontent

        # Don't scroll more than is needed
        self.mc_linepos = min(self.mc_linepos + 1, len(self.mc_content) - mc.height - 1)
        self.mcwin.refresh(self.mc_linepos, 0, mc.y, mc.x, mc.y + mc.height, mc.x + mc.width)

    def stub(self):
        return

    def move_cursor_to_userinput(self) -> None:
        """
        Moves the cursor to where the user input starts.
        """

        self.screen.move(userinput.y, userinput.x)


    def end_screen(self) -> None:
        
        self.screen.keypad(False)
        curses.flushinp()
        curses.endwin()
    

    def show_main_content(self, content: [str]) -> None:

        

        self.mc_content = content
        self.mc_linepos = 0

        mc: Region = maincontent

        self.mcwin = curses.newpad(len(content), mc.width)

        i = 0
        for line in content:
        
            self.mcwin.addstr(i, 0, line)
            i += 1
        self.mcwin.refresh(0, 0, mc.y, mc.x, mc.y + mc.height, mc.x + mc.width)
