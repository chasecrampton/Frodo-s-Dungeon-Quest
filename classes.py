import random
import numpy as np
class Colors:
    green = "\033[32m"
    yellow = "\033[33m"
    red = "\033[31m"
    bold = "\033[1m"
    reset = "\033[0m"

class Weapon: # If its long range spells, shouldn't it be a staff/wand that augments the spell?
    STAFF_TYPES = {
        'base': {
            'type': "None",
            'damage': 5
        }
    }
    
    damage = 0
    type = ''

    def __init__(self, type):
        self.update(type)

    def attack(self, direction):
        pass

    def update(self, staff):
        stats = self.STAFF_TYPES[staff]
        self.damage = stats['damage']
        self.type = stats['type']

class End:
    display = "!"

    def __init__(self) -> None:
        pass

class Obstacle:
    display = "+"

    def __init__(self) -> None:
        pass

class Player:
    display = "@"

    health = 100
    inventory = []
    damage = 10
    weapon = Weapon('base')
    position = np.array([0,0])

    def __init__(self) -> None:
        pass
    def move(self, move_direction, level_map):
        new_pos = self.position + np.array(move_direction)
        new_r, new_c = int(new_pos[0]), int(new_pos[1])

        if new_r < 0 or new_r >= len(level_map) or new_c < 0 or new_c >= len(level_map[0]):
            return False # outside map boundary

        target_tile = level_map[new_r][new_c]
        if isinstance(target_tile, (Obstacle)): # doesn't work if is a wall
            return False
        self.position = new_pos
        return True

        return False
    def add_inventory(self, item):
        self.inventory.append(item)

    def use_item(self, item):
        available = False
        for i in self.inventory:
            if(i == item):
                available = True
                i.use()
                break
        
        if(available):
            return True
        else:
            return False

    def change_health(self, x):
        self.health += x

    def equip_weapon(self, weapon):
        self.weapon = weapon

    def attack(self, direction):
        self.weapon.attack(direction)

    def p(self):
        print(self.health)
    
class Monster:
    display = "M"
    health = 10
    color = None
    position = np.array([0,0])
    type = "fairy" # delete this (and getMove and corresponding move(self) if only 1 monster type)
    def update_health(self, h):
        self.health += h

        if(self.health == 10):
            self.color = Colors.green
        elif(self.health >=5):
            self.color = Colors.yellow
        else:
            self.color = Colors.red
    def move(self, player_position, level_map):
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
        match self.type:
            case "fairy": # fairy = random movement
                return random.choice([
                    np.array([-1, 0]),
                    np.array([0, -1]),
                    np.array([1, 0]),
                    np.array([0, 1]),]) # does inclusive random integer
            case "goblin":
                a = player_position - self.position
                if abs(a[0]) >= abs(a[1]):
                    return np.array([int(np.sign(a[0])), 0]) # towards by row
                return np.array([0, int(np.sign(a[1]))]) # towards by column


class Inventory:
    HealthPacks = 0
    TotemOfUndying = 0
    Staffs = ['base']

    def add_staff(self, staff):
        self.Staffs.append(staff)

class Floor:
    display = (if (hasEffect) : "#" else " ")
    color = None
    hasEffect = False

    def spelled(self):
        hasEffect = True
        

