CHAR_CODES = {
    "-": "blank",
    "+": "obstacle",
    "M": "monster",
    "@": "amulet",
    "!": "end",
}

def read_level(type: str, num: int):
    """
    Team-written. Chase

    Writes stats to a log file at the end of each game
    """

    level = []

    with open(type, "r") as file:
        for line in file:
            line = line.split(" ")
            for space in line:
                pos_data = {

                }

                """
                “-” blank space
                “+” obstacle
                “M” monster
                “@” Amulet
                “!” level end
                """

                pos_data["type"] = CHAR_CODES[space]

                # TODO: check each character and create  

        file.close()

    return level

def display_level():
    pass

def update():
    pass