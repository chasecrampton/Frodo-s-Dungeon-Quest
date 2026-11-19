import random
import numpy as np
from typing import Any
from spell_utils import get_aoe_tiles

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
            'range': 1,
            'pierce': False,
            'spell_effect': True,
            'area_type': 'circle'
        },
        
        # --- FIRE VARIATIONS ---
        'fire_cone': {
            'type': "Fire", 'damage': 10, 'range': 3,
            'pierce': False, 'spell_effect': True, 'area_type': 'cone'
        },
        'fire_nova': {
            'type': "Fire", 'damage': 10, 'range': 2,           
            'pierce': True, 'spell_effect': True, 'area_type': 'circle'
        },
        'fire_bolt': {
            'type': "Fire", 'damage': 10, 'range': 6,           
            'pierce': False, 'spell_effect': True, 'area_type': 'line'
        },
        
        # --- LIGHTNING VARIATIONS ---
        'lightning_bolt': {
            'type': "Lightning", 'damage': 8, 'range': 4,
            'pierce': True, 'spell_effect': True, 'area_type': 'line'
        },
        'lightning_fork': {
            'type': "Lightning", 'damage': 6, 'range': 3,
            'pierce': True, 'spell_effect': True, 'area_type': 'cone'
        },
        'lightning_storm': {
            'type': "Lightning", 'damage': 5, 'range': 4,
            'pierce': True, 'spell_effect': True, 'area_type': 'circle'
        },

        # --- FROST VARIATIONS ---
        'frost_nova': {
            'type': "Frost", 'damage': 6, 'range': 2,
            'pierce': True, 'spell_effect': True, 'area_type': 'circle'
        },
        'frost_lance': {
            'type': "Frost", 'damage': 12, 'range': 5,
            'pierce': False, 'spell_effect': True, 'area_type': 'line'
        },
        'frost_cone': {
            'type': "Frost", 'damage': 8, 'range': 3,
            'pierce': True, 'spell_effect': True, 'area_type': 'cone'
        },

        # --- EARTH VARIATIONS ---
        'earth_spike': {
            'type': "Earth", 'damage': 15, 'range': 2,
            'pierce': False, 'spell_effect': True, 'area_type': 'line'
        },
        'earth_quake': {
            'type': "Earth", 'damage': 7, 'range': 3,
            'pierce': True, 'spell_effect': True, 'area_type': 'circle'
        },
        'frost_circle': {
            'type': "Frost",
            'damage': 6,
            'range': 2,
            'pierce': True,       # Hits everything in the blast radius
            'spell_effect': True,
            'area_type': 'circle'
        },
        'void_beam': {
            'type': "Void",
            'damage': 20,         # High damage
            'range': 6,           # Long range
            'pierce': False,      # Stops at the first enemy hit
            'spell_effect': True,
            'area_type': 'line'
        }
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
    area_type = 'circle'

    def __init__(self, weapon_type: str):
        self.update(weapon_type)

    def _normalize_direction(self, direction) -> np.ndarray:
        """AI-assisted. Converts a WASD string or coordinate offset into a NumPy [row, col] array."""
        if isinstance(direction, str):
            key = direction.lower()
            if key not in self.DIRECTION_MAP:
                return np.array([0,0])
            return np.array(self.DIRECTION_MAP[key])
        return np.array(direction)
    
    def _process_tile_effects(self, r: int, c: int, level_map: list[list[Any]]):
        """AI-assisted. Applies environmental spell effects (and burns loot)."""
        target_tile = level_map[r][c]
        if isinstance(target_tile, Loot):
            level_map[r][c] = Floor()
            target_tile = level_map[r][c]
            # ^this burns up the item lol. more specifically, because Item/Loot implements/subclass of Floor, 
            # it goes throught the if statement. then we just set it to floor lol.
            return
        if self.spell_effect and isinstance(target_tile, Floor):
            target_tile.spelled(True)
        return

    def attack(self, player, direction, level_map: list[list[Any]], monsters: list["Monster"])-> tuple[list, list]:
        """AI-assisted, with one line made by Jonathan. Fires an attack from the player in one direction and returns hit monsters and affected coordinates."""
        dir_vec = self._normalize_direction(direction)
        if dir_vec is None or np.array_equal(dir_vec, [0, 0]):
            return [], []

        total_damage = player.damage + self.damage #adds weapon damage + base player damage
        hit_monsters = []
        affected_tiles = get_aoe_tiles(player.position, dir_vec, self.area_type, self.range, level_map)
        
        for r, c in affected_tiles:
            if isinstance(level_map[r][c], Obstacle) and not self.pierce:
                continue

            # Optional: Stop processing tiles behind walls (basic line of sight block)
            self._process_tile_effects(r, c, level_map)

            # Check if any monsters are standing here
            for monster in list(monsters):
                if int(monster.position[0]) == r and int(monster.position[1]) == c:
                    monster.update_health(-total_damage)
                    hit_monsters.append(monster)
                    if monster.health <= 0:
                        monsters.remove(monster)
                        player.action_log.append(f"Killed a {monster.type} monster!") # LOGGER

        return hit_monsters, affected_tiles

    def update(self, staff: str):
        """Team-written.
        
        Updates the currently equipped staff to a different one.
        """
        stats = self.STAFF_TYPES[staff]
        self.damage = stats['damage']
        self.type = stats['type']
        self.range = stats.get('range', 1)
        self.pierce = stats.get('pierce', False)
        self.spell_effect = stats.get('spell_effect', False)
        self.area_type = stats.get('area_type', 'circle') # defaults to circle

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
        return f"Restored {self.heal_amount} health!"

class TotemOfUndying:
    name = "TotemOfUndying"

    def use(self, player):
        """AI-assisted. Restores a large amount of health to the player."""
        player.change_health(100)
        return "Restored 100 health!"

class StrengthPotion:
    name = "StrengthPotion"

    def use(self, player):
        """AI-assisted. Increases the player's base damage permanently."""
        player.damage += 5
        return "Increased base damage by 5!"

class Whetstone:
    name = "Whetstone"

    def use(self, player):
        """AI-assisted. Permanently increases base damage."""
        player.damage += 3
        return "Increased base damage by 3!"

class MysteryBrew:
    name = "MysteryBrew"

    def use(self, player):
        """AI-assisted. 50/50 chance to either heal you greatly or deal damage."""
        import random
        if random.random() > 0.5:
            player.change_health(20)
            return "Increased health by 20!"
        else:
            player.change_health(-15)
            return "Decreased health by 15!"

class MagicScroll:
    name = "MagicScroll"

    def use(self, player):
        """AI-assisted. Unlocks a new spell slot for the player."""
        # Find spells in the game that the player doesn't have yet
        if len(player.spell_slots) >= 4:
            return False
            
        available_spells = [spell for spell in Weapon.STAFF_TYPES.keys() if spell not in player.spell_slots]
        
        if available_spells:
            new_spell = random.choice(available_spells)
            player.spell_slots.append(new_spell)
            return f"Learned the {new_spell.capitalize()} spell!"
        else:
            # Fallback if they have all spells/this spell
            player.health += 15
            return "Already know all spells! Restored 15 health instead."
            
        return True

class Inventory:
    # Central registry of all usable items in the game
    AVAILABLE_ITEMS = {
        "HealthPack": HealthPack,
        "TotemOfUndying": TotemOfUndying,
        "StrengthPotion": StrengthPotion,
        "Whetstone": Whetstone,
        "MysteryBrew": MysteryBrew,
        "MagicScroll": MagicScroll,
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

    def use_item(self, item, player):
        """AI-assisted. Triggers the item's .use() method and decrements its count."""
        name = self._resolve_name(item)
        if self.items.get(name, 0) <= 0:
            return False

        item_instance = self.AVAILABLE_ITEMS[name]()
        result = item_instance.use(player)
        
        # If it explicitly returned False, the item failed to activate
        if result is False:
            return False
            
        self.items[name] -= 1
        
        # Return the descriptive message string instead of True
        return result

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
    damage = 10
    position = np.array([0,0])

    def __init__(self) -> None:
        self.inventory = Inventory()
        self.weapon = Weapon('base')
        self.spell_slots = ["base"]
        self.action_log: list[str] = []

    def move(self, move_direction: np.ndarray, level_map: list[list[Any]], monsters: list["Monster"]) -> bool:
        """Team-written.
        
        Moves the player in a direction. Returns True or False based on if the player was able to move.
        """

        new_pos = self.position + np.array(move_direction)
        new_r, new_c = int(new_pos[0]), int(new_pos[1])

        if new_r < 0 or new_r >= len(level_map) or new_c < 0 or new_c >= len(level_map[0]):
            return False # outside map boundary

        target_tile = level_map[new_r][new_c]
        if isinstance(target_tile, Obstacle): # doesn't work if is a wall
            return False
        for monster in monsters:
            if np.array_equal(new_pos, monster.position):
                monster.attack(self)
                return False # Movement blocked; turn ends
        else:
            # User picking up items
            if getattr(target_tile, 'item_name', None):
                self.add_to_inventory(target_tile.item_name)
                self.action_log.append(f"Picked up item: {target_tile.item_name}") # LOGGER
                # Remove item from floor
                level_map[new_r][new_c] = Floor()

        self.position = new_pos
        return True

    def add_to_inventory(self, item: str):
        """Team-written.
        
        Adds item to players inventory"""
        self.inventory.add_item(item)

    def use_item(self, item: str):
        """Team-written.
        
        If the player has the item in the inventory, use it. Returns wehter the item was used or not.
        """
        return self.inventory.use_item(item, self)
    def change_health(self, x: int):
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

    def equip_weapon(self, weapon: Weapon):
        """Team-written.
        
        Equips a weapon
        """

        self.weapon = weapon

    def attack(self, direction: np.ndarray, level_map: list[list[Any]], monsters: list["Monster"]):
        """AI-assisted. Attacks in a chosen direction and returns hit monsters and affected tile coordinates."""
        return self.weapon.attack(self, direction, level_map, monsters)
    
    def cast_spell(self, slot_index: int, direction, level_map: list[list[Any]], monsters: list) -> tuple[list, list]:
        """AI-written. Casts a spell from the designated slot index."""
        if slot_index >= len(self.spell_slots):
            return [], []
            
        spell_name = self.spell_slots[slot_index]
        self.equip_weapon(Weapon(spell_name))
        
        # Attack using the equipped spell logic
        return self.attack(direction, level_map, monsters)

    def p(self):
        """Team-written.
        
        Prints the players health."""

        print(self.health)
    
class Monster:
    map_char = "M"
    health = 30
    position = np.array([0,0])
    type = "fairy" # delete this (and getMove and corresponding move(self) if only 1 monster type)
    damage = 10
    speed = 1
    path_index = 0
    path = []
    MONSTER_STATS = {
        "fairy":      {"health": 6,  "display": "F"},
        "bat":        {"health": 8,  "display": "B"},
        "goblin":     {"health": 10, "display": "G"},
        "hound":      {"health": 12, "display": "H"},
        "spider":     {"health": 12, "display": "S"},
        "zombie":     {"health": 18, "display": "Z"},
        "trap":       {"health": 25, "display": "T"},
    }
    BAT_PATHS = [
        # Path 1: 2x2 Square (Right x2, Down x2, Left x2, Up x2)
        [np.array([0, 1]), np.array([0, 1]), np.array([1, 0]), np.array([1, 0]),
         np.array([0, -1]), np.array([0, -1]), np.array([-1, 0]), np.array([-1, 0])],
         
        # Path 2: Vertical Patrol (Down x3, Up x3)
        [np.array([1, 0]), np.array([1, 0]), np.array([1, 0]), 
         np.array([-1, 0]), np.array([-1, 0]), np.array([-1, 0])],
         
        # Path 3: Horizontal Patrol (Right x3, Left x3)
        [np.array([0, 1]), np.array([0, 1]), np.array([0, 1]), 
         np.array([0, -1]), np.array([0, -1]), np.array([0, -1])],
         
        # Path 4: Tight Circle (Right, Down, Left, Up)
        [np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0])]
    ]

    def update_health(self, h: int):
        """Team-written.
        
        Updates the monster's health."""

        self.health += h
    def chooseRandomMonster(self):
        """Team-written. Randomly selects a type and configures its attributes."""
        choices = ["fairy", "goblin", "zombie", "stationary", "bat", "hound"] # getting rid of "coward"
        self.type = random.choice(choices)
        
        if self.type == "hound": # hound moves twice
            self.speed = 2
        else:
            self.speed = 1
        if self.type == "bat":
            self.path = random.choice(self.BAT_PATHS)
            self.path_index = 0
        return self.type
    
    @property
    def display(self):
        """Team-written. Returns a unique map character based on the monster's type."""
        display_chars = {
            "fairy": "F",
            "goblin": "G",
            "zombie": "Z",
            "coward": "C",
            "trap": "T",
            "bat": "B",
            "hound": "H",
            "spider": "S"
        }
        return display_chars.get(self.type, "M")
    @property
    def color(self):
        """AI-assisted. Returns the existing monster color for its health."""
        if self.health == 10:
            return Colors.green
        if self.health >= 5:
            return Colors.yellow
        return Colors.red
    def _is_move_blocked(self, new_pos: np.ndarray, level_map: list[list[Any]], monsters: list) -> bool:
        """Team-written.
                
        See if new position is available to be moved onto"""
        new_r, new_c = int(new_pos[0]), int(new_pos[1])
        # Check boundaries
        if new_r < 0 or new_r >= len(level_map) or new_c < 0 or new_c >= len(level_map[0]):
            return True
        # Check if is Floor
        if not isinstance(level_map[new_r][new_c], Floor):
            return True
        # Check collision with another monster
        for other in monsters:
            if other is not self and np.array_equal(new_pos, other.position):
                return True
                
        return False
    def move(self, player: "Player", level_map: list[list[Any]], monsters: list["Monster"]) -> bool:
        """Team-written.
        
        Moves based on player position, map, and type of monster"""

        for step in range(self.speed):
            move_direction = self.getMove(player.position)
            
            # If the monster wants to stay still, skip processing
            if np.array_equal(move_direction, [0, 0]):
                break
                
            new_pos = self.position + np.array(move_direction)
            new_r, new_c = int(new_pos[0]), int(new_pos[1])

            # Check player collision
            if np.array_equal(new_pos, player.position):
                self.attack(player) 
                return False # Attack the player and end movement turn. Returns fallse because attacked but didn't move
            if self._is_move_blocked(new_pos, level_map, monsters):
                return False
                
            # else Move successful; update position
            self.position = new_pos
            
        return True
    
    def attack(self, player):
        """Team-written.
        
        Decreases player health"""
        player.change_health(-self.damage)
        player.action_log.append(f"Got hurt by a {self.type} monster for {self.damage} damage!") # LOGGER
        return
    
    def getMove(self, player_position = [0,0]):
        """Team-written. Jonathan
        
        Gets a move based on monster type"""

        match self.type:
            case "trap":
                return np.array([0, 0])
                
            case "bat":
                # Cycle through the predefined path array
                move = self.path[self.path_index % len(self.path)]
                self.path_index += 1
                return move
                
            case "hound":
                # Hound uses goblin logic, but its speed=2 allows it to execute it twice
                a = player_position - self.position
                if abs(a[0]) >= abs(a[1]):
                    return np.array([int(np.sign(a[0])), 0])
                return np.array([0, int(np.sign(a[1]))])
                
            case "fairy": 
                return random.choice([
                    np.array([-1, 0]), np.array([0, -1]),
                    np.array([1, 0]), np.array([0, 1])
                ])
                    
            case "goblin": 
                a = player_position - self.position
                if abs(a[0]) >= abs(a[1]):
                    return np.array([int(np.sign(a[0])), 0]) 
                return np.array([0, int(np.sign(a[1]))]) 
                
            case "zombie": 
                a = player_position - self.position
                options = []
                if a[0] != 0: options.append(np.array([int(np.sign(a[0])), 0]))
                if a[1] != 0: options.append(np.array([0, int(np.sign(a[1]))]))
                return random.choice(options) if options else np.array([0, 0])
            case "spider":
                # Moves diagonally (and orthogonally when aligned) directly toward the player
                a = player_position - self.position
                return np.array([int(np.sign(a[0])), int(np.sign(a[1]))])
            case "coward": 
                a = self.position - player_position # Reversed vector
                if abs(a[0]) >= abs(a[1]) and a[0] != 0:
                    return np.array([int(np.sign(a[0])), 0])
                elif a[1] != 0:
                    return np.array([0, int(np.sign(a[1]))])
                return random.choice([
                    np.array([-1, 0]), np.array([0, -1]),
                    np.array([1, 0]), np.array([0, 1])
                ])
            case _: # if monster name didn't exist, default to stationary
                return np.array([0,0])

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

class Loot(Floor):
    display = "?"
    
    def __init__(self, item_name):
        super().__init__()
        self.item_name = item_name