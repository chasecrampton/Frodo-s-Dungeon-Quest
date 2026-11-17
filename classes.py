import random
import numpy as np
class Colors:
    green = "\033[32m"
    yellow = "\033[33m"
    red = "\033[31m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    bold = "\033[1m"
    reset = "\033[0m"

class Weapon:
    STAFF_TYPES = {
        'base': {
            'type': "None",
            'damage': 5,
            'range': 1,          # Adjacent tile only
            'pierce': False,     # Stops at the first monster hit
            'spell_effect': False
        },
        # Example future staffs your team can add:
        # 'fire': {
        #     'type': "Fire",
        #     'damage': 10,
        #     'range': 3,
        #     'pierce': False,
        #     'spell_effect': True  # Triggers Floor.spelled() along the path
        # },
        # 'lightning': {
        #     'type': "Lightning",
        #     'damage': 8,
        #     'range': 4,
        #     'pierce': True,       # Hits every monster in a line
        #     'spell_effect': False
        # }
    }

    DIRECTION_MAP = {
        'w': (-1, 0),
        'a': (0, -1),
        's': (1, 0),
        'd': (0, 1),
    }

    damage = 0
    type = ''
    range = 1
    pierce = False
    spell_effect = False

    def __init__(self, type):
        self.update(type)

    def _normalize_direction(self, direction):
        """AI-assisted. Converts a WASD string or coordinate offset into a NumPy [row, col] array."""
        if isinstance(direction, str):
            key = direction.lower()
            if key not in self.DIRECTION_MAP:
                return None
            return np.array(self.DIRECTION_MAP[key])
        return np.array(direction)

    def attack(self, player, direction, level_map, monsters):
        """AI-assisted. Fires an attack from the player in one direction and returns hit monsters and affected coordinates."""
        dir_vec = self._normalize_direction(direction)
        if dir_vec is None or np.array_equal(dir_vec, [0, 0]):
            return [], []

        total_damage = player.damage + self.damage
        hit_monsters = []
        affected_tiles = []

        for step in range(1, self.range + 1):
            target_pos = player.position + (dir_vec * step)
            r, c = int(target_pos[0]), int(target_pos[1])

            # Stop if the attack reaches the edge of the map
            if r < 0 or r >= len(level_map) or c < 0 or c >= len(level_map[0]):
                break

            target_tile = level_map[r][c]

            # Obstacles block attacks
            if isinstance(target_tile, Obstacle):
                break

            affected_tiles.append((r, c))

            # Optional: mark floor tiles with '#' if the staff leaves a spell effect
            if self.spell_effect and isinstance(target_tile, Floor):
                target_tile.spelled(True)

            # Check for any monster standing on this tile
            monster_hit_here = False
            for monster in list(monsters):
                if int(monster.position[0]) == r and int(monster.position[1]) == c:
                    monster.update_health(-total_damage)
                    hit_monsters.append(monster)
                    monster_hit_here = True
                    if monster.health <= 0:
                        monsters.remove(monster)

            # Stop after hitting a monster unless the staff pierces
            if monster_hit_here and not self.pierce:
                break

        return hit_monsters, affected_tiles

    def update(self, staff):
        """Team-written.
        
        Updates the currently equipped staff to a different one.
        """
        stats = self.STAFF_TYPES[staff]
        self.damage = stats['damage']
        self.type = stats['type']
        self.range = stats.get('range', 1)
        self.pierce = stats.get('pierce', False)
        self.spell_effect = stats.get('spell_effect', False)

class End:
    display = "!"

    def __init__(self) -> None:
        pass

class Obstacle:
    display = "+"

    def __init__(self) -> None:
        pass


class HealthPack:
    name = "HealthPack"
    heal_amount = 25

    def use(self, player):
        """AI-assisted. Restores health to the player."""
        player.change_health(self.heal_amount)


class TotemOfUndying:
    name = "TotemOfUndying"

    def use(self, player):
        """AI-assisted. Restores a large amount of health to the player."""
        player.change_health(50)


class Inventory:
    # Central registry of all usable items in the game
    AVAILABLE_ITEMS = {
        "HealthPack": HealthPack,
        "TotemOfUndying": TotemOfUndying,
    }

    def __init__(self):
        """AI-assisted. Initializes the running tally to 0 for all available items and sets default staffs."""
        self.items = {name: 0 for name in self.AVAILABLE_ITEMS}
        self.staffs = ['base']

    def _resolve_name(self, item):
        """AI-assisted. Extracts the item name string from a string, item class, or item instance."""
        if isinstance(item, str):
            return item
        return item.name

    def add_item(self, item, amount=1):
        """AI-assisted. Increments the running tally for the given item."""
        name = self._resolve_name(item)
        if name not in self.items:
            raise ValueError(f"Unknown item: {name}")
        self.items[name] += amount

    def use_item(self, item, player=None):
        """AI-assisted. Triggers the item's .use() method and decrements its count if available."""
        name = self._resolve_name(item)
        if self.items.get(name, 0) <= 0:
            return False

        item_instance = self.AVAILABLE_ITEMS[name]()
        item_instance.use(player)
        self.items[name] -= 1
        return True

    def get_count(self, item):
        """AI-assisted. Returns the current tally for a specific item."""
        name = self._resolve_name(item)
        return self.items.get(name, 0)

    def add_staff(self, staff):
        """AI-assisted. Adds a staff to the inventory if it is not already owned."""
        if staff not in self.staffs:
            self.staffs.append(staff)

    def __str__(self):
        """AI-assisted. Formats the inventory tallies and staffs into a single string for terminal output."""
        tally_str = " | ".join(f"{name}: {count}" for name, count in self.items.items())
        return f"{tally_str} | Staffs: {', '.join(self.staffs)}"

class Player:
    display = "@"

    health = 100
    inventory = Inventory()
    damage = 10
    weapon = Weapon('base')
    position = np.array([0,0])

    def __init__(self) -> None:
        pass

    def move(self, move_direction, level_map):
        """Team-written.
        
        Moves the player in a direction. Returns True or False based on if the player was able to move.
        """

        new_pos = self.position + np.array(move_direction)
        new_r, new_c = int(new_pos[0]), int(new_pos[1])

        if new_r < 0 or new_r >= len(level_map) or new_c < 0 or new_c >= len(level_map[0]):
            return False # outside map boundary

        target_tile = level_map[new_r][new_c]
        if isinstance(target_tile, (Obstacle)): # doesn't work if is a wall
            return False
        
        self.position = new_pos
        return True

    def add_to_inventory(self, item):
        """Team-written.
        
        Adds item to players inventory"""
        self.inventory.add_item(item)

    def use_item(self, item):
        """Team-written.
        
        If the player has the item in the inventory, use it. Returns wehter the item was used or not.
        """
        self.inventory.use_item(item)
    def change_health(self, x):
        """Team-written.
        
        Updates players health
        """
        self.health += x

    @property
    def color(self):
        """AI-assisted. Returns the player's color at their current health."""
        if self.health <= 15:
            return Colors.red
        if self.health <= 40:
            return Colors.yellow
        return Colors.green

    def equip_weapon(self, weapon):
        """Team-written.
        
        Equips a weapon
        """

        self.weapon = weapon

    def attack(self, direction, level_map, monsters):
        """AI-assisted. Attacks in a chosen direction and returns hit monsters and affected tile coordinates."""
        return self.weapon.attack(self, direction, level_map, monsters)

    def p(self):
        """Team-written.
        
        Prints the players health."""

        print(self.health)
    
class Monster:
    display = "M"
    health = 10
    position = np.array([0,0])
    type = "fairy" # delete this (and getMove and corresponding move(self) if only 1 monster type)

    def update_health(self, h):
        """Team-written.
        
        Updates the monster's health."""

        self.health += h

    @property
    def color(self):
        """AI-assisted. Returns the existing monster color for its health."""
        if self.health == 10:
            return Colors.green
        if self.health >= 5:
            return Colors.yellow
        return Colors.red

    def move(self, player_position, level_map):
        """Team-written.
        
        Moves based on player position and map"""

        move_direction = self.getMove(player_position)
        new_pos = self.position + np.array(move_direction)
        new_r, new_c = int(new_pos[0]), int(new_pos[1])

        if new_r < 0 or new_r >= len(level_map) or new_c < 0 or new_c >= len(level_map[0]):
            return False # outside map boundary

        target_tile = level_map[new_r][new_c]
        if isinstance(target_tile, (Obstacle)): # doesn't work if is a wall
            return False
        self.position = new_pos
        return True

    def getMove(self, player_position = [0,0]):
        """Team-written.
        
        Gets a move based on monster type"""

        match self.type:
            case "fairy": # fairy = random movement
                return random.choice([
                    np.array([-1, 0]),
                    np.array([0, -1]),
                    np.array([1, 0]),
                    np.array([0, 1])]) # does inclusive random integer
            case "goblin":
                a = player_position - self.position
                if abs(a[0]) >= abs(a[1]):
                    return np.array([int(np.sign(a[0])), 0]) # towards by row
                return np.array([0, int(np.sign(a[1]))]) # towards by column

class Floor:
    color = None
    hasEffect = False
    display = " "

    def spelled(self, b = True):
        """Team-written.
        
        \"Spells\" a tile. Or unspells it by passing False."""

        self.hasEffect = b
        self.update_display()
        
    def update_display(self):
        """Team-written.
        
        Updates the tile's display based on if it has a spell or not."""

        self.display = "#" if self.hasEffect else " "
