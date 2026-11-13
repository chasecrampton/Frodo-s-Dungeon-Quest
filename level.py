import classes as cls
import numpy as np


class Level:
    CHAR_CLASSES = {
        "-": cls.Floor,
        cls.Obstacle.display: cls.Obstacle,
        cls.Monster.display: cls.Monster,
        cls.End.display: cls.End,
        cls.Player.display: cls.Player
    }
    map = []
    player: cls.Player
    monsters: list[cls.Monster]
    
    def __init__(self, level_file: str, player: cls.Player):
        self.map = self.read_level(level_file)
        self.player = player
        monsters = []

    def read_level(self, filepath: str):
        """
        Team-written.
        
        Reads a level file and returns a map with objects of each
        """

        map = []

        with open(filepath, "r") as file:
            for r, line in enumerate(file):
                row = []
                line = line.strip()
                line = line.split(" ")
                for c, space in enumerate(line): # tile_type? then we access the other more specific stuff later
                    if space == cls.Player.display:
                        # don't create another player object
                        self.player.position = np.array([r, c])
                        row.append(self.player)
                        continue
                    if space == cls.Monster.display:
                        monster = cls.Monster()
                        monster.position = np.array([r,c])
                        monster.type = "fairy"
                        self.monsters.append(monster)
                    entity = self.CHAR_CLASSES[space]()
                    row.append(entity)

                map.append(row)
                
            file.close()
        return map

    def display_level(self):
        for row in self.map:
            for col in row:
                print(col.display_character, end = "") # with color
            print() # new line for each row
            
        # TODO: when printing, use blank space " " instead of "-"

    def update(self): # 
        '''   UPDATE   '''
        input = self.player.get_input() # gets input (wasd, inventory, etc.)
        if not isValidInput(input): # checks against a list of inputs
            # TODO: print tell player "invalid input" and "h for help"
            return # doesn't update if invalid input
        
        if input == "h" or input == "help":
            # TODO: make and print a help screen
            pass
        if input_is_movement(input) # TODO: make method input_is_movement(string) bool   check if input is wasd 
            move_direction = wasd_to_array(input) # TODO: make method wasd_to_array(string) turns wasd to np.array [-1,0] [0,-1] [1,0] [0,1] (in [r,c] format)
            self.change_grid(player.position, cls.Floor)
            self.player.move(move_direction)
            self.change_grid(self.player.position, self.player)

            for monster in self.monsters:
                self.change_grid(monster.position, cls.Floor) # remove the "M" # TODO: make method change_grid (this is a bit complicated)
                monster.move(self.player.position) # new monster position, depends on what type of move_towards function the monster has (can move towards player, randomly, or stay still)
                self.change_grid(monster.position, monster) # monster.position now uses new monster position
            
            return # stops update because move is done
        
        if input == "inventory" or input == "status":
            # display inventory, equipment, and status
            pass
        pass
    def change_grid(self, position, entity):
        row, col = position
        self.map[row][col] = entity