# Heavy WIP
import curses
import textwrap

from data import Card, session_objects
from screen import Region, r_turn_counter, r_game_version, r_game_mode, r_point_total, r_hand_cards, r_user_input, r_main_content, r_history
from screen import r_money_in_hand, r_actions_left, r_purchases_left, r_bonus_money, r_money_left

# Screen requirements
minimum_width = 130
minimum_height = 30

class Screen:

    screen = None
    mcwin = None
    handcard = None
    hist = None

    mc_content: [str] = []
    mc_linepos: int = 0
    hist_content: [(str, int)] = []


    def __init__(self):
        self.screen = curses.initscr()

    def init_screen(self) -> None:

        # CURSES INIT
        curses.start_color()
        self.screen.keypad(True)
        self.screen.clear()

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
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
        self.clear_main_content()
        self.clear_history()

        self.screen.addstr(r_game_mode.y, r_game_mode.x, session_objects.s_game_mode.rjust(r_game_mode.width, " "))
        self.screen.addstr(r_game_version.y, r_game_version.x, session_objects.s_game_version.rjust(r_game_version.width, " "))
        self.hist = curses.newpad(r_history.height, r_history.width)
        self.screen.move(27, 5)

    def update_hand_card(self, cards: [str]) -> None:


        self.handcard = curses.newwin(r_hand_cards.height, r_hand_cards.width, r_hand_cards.y, r_hand_cards.x)

        self.handcard.clear()

        i = 0
        for line in cards:
            self.handcard.addstr(i, 0, line)
            i += 1 

        self.handcard.refresh()

    def update_top_dynamic_values(self, deck_value: int) -> None:

        self.screen.addstr(r_turn_counter.y, r_turn_counter.x, str(session_objects.s_turn_counter).rjust(r_turn_counter.width, " "))
        self.screen.addstr(r_point_total.y, r_point_total.x, str(deck_value).rjust(r_point_total.width, " "))

        
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
                self.screen.move(r_user_input.y, r_user_input.x + index)

            elif c == curses.KEY_RIGHT:

                # Make sure we don't leave the designated space
                index = min(len(res), index + 1)

                # Move the cursor accordingly
                self.screen.move(r_user_input.y, r_user_input.x + index)


            # Backspace key:
            elif c == curses.KEY_BACKSPACE or c == 127:

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
                    if len(res) >= r_user_input.width:
                        res[index] = chr(c)
                    else:
                        
                        # Only add to input arr if in this string
                        if (chr(c) in "abcdefghijklmnopqrstuvwxyz1234567890, "):
                            res.insert(index, chr(c))

                            # Get the new index
                            index = min(r_user_input.width - 1, index + 1)
                
                except ValueError:
                    pass


            # Print new string, and clear one character more in case some odd character is printed
            # e.g. when deleting the last character, "^?" gets printed making "?" appear right beside the input
            # where the user can't get to it
            self.screen.addstr(r_user_input.y, r_user_input.x, "".join(res).ljust(r_user_input.width, "_") + " ")

            # Move cursor back to index, as addstr moves it
            self.screen.move(r_user_input.y, r_user_input.x + index)
            
            # Refresh
            self.screen.refresh()
                
            # Wait for new character
            c = self.screen.getch()
        
        # Replace user input with underscores again
        self.screen.addstr(r_user_input.y, r_user_input.x, "_" * r_user_input.width)

        # Move cursor back to the start.
        self.move_cursor_to_userinput()

        self.screen.refresh()

        return "".join(res)

    def scroll_up(self) -> None:
        if self.mcwin is None: return

        mc: Region = r_main_content

        # Don't scroll more than is needed
        self.mc_linepos = max(self.mc_linepos - 1, 0)

        # Refresh the main content pad, start showing content from the new starting line.
        self.mcwin.refresh(self.mc_linepos, 0, mc.y, mc.x, mc.y + mc.height, mc.x + mc.width)

    def scroll_down(self) -> None:
        if self.mcwin is None: return

        mc: Region = r_main_content

        # Don't scroll more than is needed
        self.mc_linepos = min(self.mc_linepos + 1, len(self.mc_content) - mc.height - 1)
        self.mcwin.refresh(self.mc_linepos, 0, mc.y, mc.x, mc.y + mc.height, mc.x + mc.width)

    def move_cursor_to_userinput(self) -> None:
        """
        Moves the cursor to where the user input starts.
        """

        self.screen.move(r_user_input.y, r_user_input.x)

    def end_screen(self) -> None:
        
        self.screen.keypad(False)
        curses.flushinp()
        curses.endwin()  

    def clear_main_content(self) -> None:
        self.mc_content = []
        self.mc_linepos = 0
        self.mcwin = curses.newwin(r_main_content.height + 1, r_main_content.width, r_main_content.y, r_main_content.x)
        self.mcwin.clear()
        self.mcwin.refresh()

    def show_main_content(self, content: []) -> None:
        self.clear_main_content()
        self.mc_content = content
        self.mc_linepos = 0

        mc: Region = r_main_content

        self.mcwin = curses.newpad(len(content), mc.width)

        i = 0
        for line in content:

            # if a color is provided
            if isinstance(line, tuple):
                self.mcwin.addstr(i, 0, line[0], curses.color_pair(line[1]))
            else:
                self.mcwin.addstr(i, 0, line)
            i += 1
        self.mcwin.refresh(0, 0, mc.y, mc.x, mc.y + mc.height, mc.x + mc.width)

    def clear_history(self) -> None:
        
        # Empty content array
        self.hist_content = []
        
        # Make window over the history content region, and clear it
        self.hist = curses.newwin(r_history.height, r_history.width, r_history.y, r_history.x)
        self.hist.clear()
        self.hist.refresh()

    def log(self, message: str, color: int=0) -> None:
        """
        Logs a message to the history window. Text gets wrapped automatically.
        """

        # Format message
        wrapper  = textwrap.TextWrapper(width= r_history.width)
        self.hist_content = self.hist_content + [(i, color) for i in wrapper.wrap(message)]

        self.hist = curses.newpad(len(self.hist_content), r_history.width)

        i = 0
        for line in self.hist_content:
            self.hist.addstr(i, 0, line[0], curses.color_pair(line[1]))
            i += 1

        pad_minrow = max(0, len(self.hist_content) - r_history.height)
        self.hist.refresh(max(0, pad_minrow), 0,  r_history.y, r_history.x, r_history.y + r_history.height, r_history.x + r_history.width)

    def update_turn_overview(self, money: int, actions: int, purchases: int, bonus: int, left: int) -> None:
        
        self.screen.addstr(
            r_money_in_hand.y, r_money_in_hand.x, 
            str(money).ljust(r_money_in_hand.width, " "), curses.color_pair(2 if money == 0 else 0)
        )
        self.screen.addstr(
            r_actions_left.y, r_actions_left.x, 
            str(actions).ljust(r_actions_left.width, " "), curses.color_pair(2 if actions == 0 else 1 if actions > 1 else 0)
        )
        self.screen.addstr(
            r_purchases_left.y, r_purchases_left.x, 
            str(purchases).ljust(r_purchases_left.width, " "), curses.color_pair(2 if purchases == 0 else 1 if purchases > 1 else 0)
        )
        self.screen.addstr(
            r_bonus_money.y, r_bonus_money.x, 
            str(bonus).ljust(r_bonus_money.width, " "), curses.color_pair(0 if bonus == 0 else 1)
        )
        self.screen.addstr(
            r_money_left.y, r_money_left.x, 
            str(left).ljust(r_money_left.width, " "), curses.color_pair(2 if left == 0 else 0)
        )
        self.screen.refresh()
