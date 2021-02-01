# Card object
class Card:
    name: str = ""
    cost: int = 0
    cardtype: str = ""
    value: int = 0
    action: str = ""
    description: str = ""

    def __init__(self, d: dict): 
        self.__dict__.update(d) 

