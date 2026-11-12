CHAR_CODES = {
    "-": {
        "type": "blank",
        "health": ""
    },
    "+": {
        "type": "obstacle"
    },
    "M": {
        "type": "monster"
    },
    "!": {
        "type": "end"
    },
    "@": {
        "type":"player"
    }
}

class Level:
    

def read_level(type: str, num: int):
    """
    Team-written. Chase

    Writes stats to a log file at the end of each game
    """

    level = []

    with open(type, "r") as file:
        for line in file:
            row = []
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

                row.append(pos_data)
        file.close()

    return level

def display_level():
    monster_positions = current_level.get_monster_positions()
    for monster_position in monster_positions {
        
    }
    current_level.get_player_position()
    if (current_level.amulet_is_taken()) {
        amulet_location = " "
    }
    pass
    # TODO: when printing, use blank space " " instead of "-"

def update():

    pass