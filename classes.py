class Dog:
    # Class attribute (shared by all dogs)
    species = "Canis familiaris"

    # Constructor method
    def __init__(self, name, age):
        # Instance attributes (unique to each dog)
        self.name = name
        self.age = age

    # Instance method
    def bark(self):
        return f"{self.name} says woof!"
    
# Creating objects (instances) of the Dog class
dog1 = Dog("Buddy", 3)
dog2 = Dog("Bella", 5)

# Accessing attributes and calling methods
print(dog1.name)       # Output: Buddy
print(dog2.bark())     # Output: Bella says woof!
print(dog1.species)

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

    def __init__(self) -> None:
        pass

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

    def update_health(self, h):
        self.health += h

        if(self.health == 10):
            self.color = Colors.green
        elif(self.health >=5):
            self.color = Colors.yellow
        else:
            self.color = Colors.red

class Inventory:
    HealthPacks = 0
    TotemOfUndying = 0
    Staffs = ['base']

    def add_staff(self, staff):
        self.Staffs.append(staff)



