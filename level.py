import classes as cls
import numpy as np
from pathlib import Path
import random

def wasd_to_array(key):
    """AI-assisted. Converts a WASD key to a row and column offset."""
    directions = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}
    if key in directions:
        return np.array(directions[key])


class Level:
    CHAR_CLASSES = {
        "-": cls.Floor,
        cls.Obstacle.display: cls.Obstacle,
        cls.Monster.map_char: cls.Monster,
        cls.End.display: cls.End,
        cls.Player.display: cls.Player
    }
    map = []
    player: cls.Player
    monsters: list[cls.Monster]
    
    def __init__(self, level_file: str | Path, player: cls.Player):
        """Team-written. Chase

        Initializes the level class.
        """
        self.player = player
        self.monsters = []
        self.map = self.read_level(str(level_file))
        if isinstance(level_file, str):
            self.name = level_file
        else:
            self.name = level_file.name

    def read_level(self, filepath: str):
        """
        Team-written. Chase, Jonathan
        
        Reads a level file and returns a map with objects of each
        """

        map = []

        with open(filepath, "r") as file:
            for r, line in enumerate(file):
                row = []
                line = line.split()
                for c, space in enumerate(line): # tile_type? then we access the other more specific stuff later
                    if space == cls.Player.display:
                        # don't create another player object
                        self.player.position = np.array([r, c])
                        row.append(cls.Floor())
                        continue
                    if space == cls.Monster.map_char:
                        monster = cls.Monster()
                        monster.position = np.array([r,c])
                        monster.type = monster.chooseRandomMonster()
                        self.monsters.append(monster)
                        if monster.health <= 0:
                            self.monsters.remove(monster)
                        row.append(cls.Floor())
                        continue
                    if space == "?":
                        # Pick a random item name from the registered items
                        item_pool = list(cls.Inventory.AVAILABLE_ITEMS.keys())
                        random_item = random.choice(item_pool)
                        row.append(cls.Loot(random_item))
                        continue
                    entity = self.CHAR_CLASSES[space]()
                    row.append(entity)

                map.append(row)
                
            file.close()
        return map

    def visible_entities(self):
        """AI-assisted. Returns the topmost entity at each occupied position."""
        return {tuple(entity.position): entity for entity in [*self.monsters, self.player]}

    def map_text(self):
        """AI-assisted. Draws moving entities over the character map."""
        rows = [[tile.display for tile in row] for row in self.map]
        for (row, col), entity in self.visible_entities().items():
            rows[row][col] = entity.display
        return "\n".join(" ".join(row) for row in rows)

    def display_level(self):
        """AI-assisted. Prints the character map in the terminal."""
        print(self.map_text())

    def update(self, key):
        """AI-assisted. Advances the level after a successful player move."""
        direction = wasd_to_array(key)
        if direction is None or not self.player.move(direction, self.map, self.monsters):
            return

        for monster in self.monsters:
            monster.move(self.player, self.map, self.monsters)

    def change_grid(self, position, entity):
        """
        Team-written. Jonathan

        Changes the position of an entity.
        """

        row, col = position
        self.map[row][col] = entity
    def clear_spell_effects(self):
        """Team-written. Jonathan
        
        Clears all temporary spell effects from the floor."""
        for row in self.map:
            for tile in row:
                if isinstance(tile, cls.Floor) and getattr(tile, 'hasEffect', False):
                    tile.spelled(False)