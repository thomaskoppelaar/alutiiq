class Region:

    y: int = -1
    x: int = -1
    height: int = -1
    width: int = -1

    def __init__(self: int, y: int, x: int, height: int, width: int):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

# Dynamic Values

r_turn_counter: Region = Region(1, 34, 1, 3)
r_game_version: Region = Region(1, 18, 1, 7)
r_game_mode: Region = Region(1, 46, 1, 15)
r_point_total: Region = Region(1, 71, 1, 3)
r_money_in_hand: Region = Region(21, 18, 1, 3)
r_actions_left: Region = Region(18, 16, 1, 2)
r_purchases_left: Region = Region(19, 18, 1, 2)
r_bonus_money: Region = Region(20, 15, 1, 2)
r_money_left: Region = Region(17, 15, 1, 3)

# Dynamic Regions (bigger than one line)
r_hand_cards: Region = Region(4, 3, 10, 21)
r_user_input: Region = Region(27, 5, 1, 17)
r_main_content: Region = Region(3, 28, 25, 50)
r_history: Region = Region(3, 81, 21, 47)
