

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

turncounter: Region = Region(1, 34, 1, 3)
gameversion: Region = Region(1, 18, 1, 7)
gamemode: Region = Region(1, 46, 1, 15)
pointtotal: Region = Region(1, 71, 1, 3)

# Dynamic Regions

handcards: Region = Region(4, 3, 10, 21)
userinput: Region = Region(27, 5, 1, 17)
maincontent: Region = Region(3, 28, 25, 50)