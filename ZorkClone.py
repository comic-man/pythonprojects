import random


# Define the player class
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 10
        self.inventory = []
        self.gold = 0

    def attack(self, enemy):
        if self.health > 0:
            damage = self.attack_power
            enemy.health -= damage
            print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        else:
            print(f"{self.name} is too weak to attack.")

    def pick_up(self, item):
        if isinstance(item, Gold):
            self.gold += item.amount
            print(f"{self.name} picks up {item.amount} gold pieces.")
        else:
            self.inventory.append(item)
            if isinstance(item, Weapon):
                self.attack_power += item.attack_boost
            print(f"{self.name} picks up {item.name}")

    def use_potion(self):
        for item in self.inventory:
            if isinstance(item, Potion):
                self.health = 100
                self.inventory.remove(item)
                print(f"{self.name} uses a potion and restores health to full.")
                return
        print("No potions in inventory.")

    def show_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print(f"- {item.name}")
        print(f"Gold: {self.gold}")

    def has_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                return True
        return False

    def has_shield(self):
        return self.has_item("Shield")

    def reduce_damage(self, damage):
        if self.has_shield():
            damage -= 5
            print(f"The shield reduces the damage by 5.")
        return max(damage, 0)


# Define the enemy class
class Enemy:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, player):
        if self.health > 0:
            damage = player.reduce_damage(self.attack_power)
            player.health -= damage
            print(f"{self.name} attacks {player.name} for {damage} damage!")
        else:
            print(f"{self.name} is defeated and cannot attack.")


# Define the item class
class Item:
    def __init__(self, name):
        self.name = name


# Define the weapon class, inheriting from item
class Weapon(Item):
    def __init__(self, name, attack_boost):
        super().__init__(name)
        self.attack_boost = attack_boost


# Define the shield class, inheriting from item
class Shield(Item):
    def __init__(self, name):
        super().__init__(name)


# Define the potion class, inheriting from item
class Potion(Item):
    def __init__(self, name):
        super().__init__(name)


# Define the gold class
class Gold(Item):
    def __init__(self, amount):
        super().__init__(f"Gold ({amount} pieces)")
        self.amount = amount


# Define the riddle class
class Riddle:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def ask(self):
        print(self.question)
        user_answer = input("Your answer: ").strip().lower()
        return user_answer == self.answer.strip().lower()


# Define the game location
class Location:
    def __init__(self, description, has_riddle=False):
        self.description = description
        self.items = []
        self.enemies = []
        self.has_riddle = has_riddle
        self.riddle = None
        self.person = None

    def enter(self):
        print(self.description)
        if self.items:
            print("You see the following items:")
            for index, item in enumerate(self.items):
                print(f"{index + 1}. {item.name}")
        if self.enemies:
            print("You encounter the following enemies:")
            for enemy in self.enemies:
                print(f"- {enemy.name}")
        if self.has_riddle and self.person:
            print(f"You meet {self.person}. They ask you a riddle.")

    def select_item(self):
        if not self.items:
            print("There are no items to pick up.")
            return None
        while True:
            try:
                choice = int(input("Enter the number of the item you want to pick up: ")) - 1
                if 0 <= choice < len(self.items):
                    return self.items.pop(choice)
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Invalid input. Enter a number.")


# Define the game map
class GameMap:
    def __init__(self):
        self.locations = {
            "forest": Location("You are in a dark forest. Paths lead north and east."),
            "cave": Location(
                "You are in a damp cave. Paths lead south and west. You see the skeleton of a dead knight."),
            "castle": Location("You are in a ruined castle. Paths lead south and east."),
            "village": Location("You are in an abandoned village. Paths lead west."),
            "forest clearing": Location("You are in a forest clearing. Paths lead north and south."),
            "riddle room": Location("You are in a room with a wise person. Paths lead east.", has_riddle=True)
        }
        # Add items to locations
        self.locations["forest"].items.append(Weapon("Sword", 5))
        self.locations["cave"].items.append(Item("Torch"))
        self.locations["cave"].items.append(Gold(50))
        self.locations["cave"].items.append(Shield("Shield"))
        self.locations["castle"].items.append(Item("Key"))
        # Add enemies to locations
        self.locations["village"].enemies.append(Enemy("Goblin", 30, 5))
        self.locations["castle"].enemies.append(Enemy("Dragon", 100, 20))
        self.locations["forest clearing"].enemies.append(Enemy("Witch", 50, 10))
        self.locations["cave"].enemies.append(Enemy("Troll", 40, 8))

        # Add riddle and person to the riddle room
        self.locations["riddle room"].riddle = random.choice([
            Riddle("What has keys but can't open locks?", "piano"),
            Riddle("What has to be broken before you can use it?", "egg"),
            Riddle("I’m tall when I’m young, and I’m short when I’m old. What am I?", "candle"),
            Riddle("What month of the year has 28 days?", "all of them"),
            Riddle("What is full of holes but still holds water?", "sponge")
        ])
        self.locations["riddle room"].person = "Fezzik the Sicilian"

        # Randomly place two potions in two different rooms
        available_locations = list(self.locations.values())
        random.sample(available_locations, 2)[0].items.append(Potion("Potion"))
        random.sample(available_locations, 2)[1].items.append(Potion("Potion"))

    def move(self, player, current_location, direction):
        if current_location == "forest":
            if direction == "north":
                return "cave"
            elif direction == "east":
                return "village"
            elif direction == "south":
                return "forest clearing"
        elif current_location == "cave":
            if direction == "south":
                return "forest"
            elif direction == "west":
                return "castle"
        elif current_location == "castle":
            if direction == "south":
                return "forest"
            elif direction == "east":
                # Check if the dragon is defeated and player has the key before moving to the riddle room
                if not any(enemy.name == "Dragon" for enemy in self.locations["castle"].enemies):
                    if player.has_item("Key"):
                        return "riddle room"
                    else:
                        print("You need the key to enter the riddle room.")
                        return current_location
                else:
                    print("The dragon blocks your path! Defeat it first.")
                    return current_location
        elif current_location == "village":
            if direction == "west":
                return "forest"
        elif current_location == "forest clearing":
            if direction == "north":
                return "forest"
            elif direction == "south":
                return "cave"
        elif current_location == "riddle room":
            if direction == "east":
                return "village"
        print("You can't go that way.")
        return current_location


# Main game loop
def main():
    player = Player(input("Enter your name: "))
    game_map = GameMap()
    current_location = "forest"

    while True:
        location = game_map.locations[current_location]
        location.enter()

        if location.has_riddle:
            if location.riddle.ask():
                print("You have answered correctly! You may pass.")
            else:
                print("Incorrect answer! You cannot pass.")
                continue

        action = input("What do you want to do? (move, attack, pick up, inventory, use potion, quit): ").strip().lower()

        if action == "move":
            direction = input("Which direction? (north, south, east, west): ").strip().lower()
            new_location = game_map.move(player, current_location, direction)
            current_location = new_location
        elif action == "attack":
            if location.enemies:
                player.attack(location.enemies[0])
                print(f"{location.enemies[0].name}'s health: {location.enemies[0].health}")
                if location.enemies[0].health <= 0:
                    print(f"{location.enemies[0].name} is defeated!")
                    location.enemies.pop(0)
                else:
                    location.enemies[0].attack(player)
                    print(f"{player.name}'s health: {player.health}")
                    if player.health <= 0:
                        print("You have been defeated!")
                        break
            else:
                print("There is nothing to attack here.")
        elif action == "pick up":
            item = location.select_item()
            if item:
                player.pick_up(item)
        elif action == "inventory":
            player.show_inventory()
        elif action == "use potion":
            player.use_potion()
        elif action == "quit":
            print("Thanks for playing!")
            break
        else:
            print("Invalid action. Try again.")


if __name__ == "__main__":
    main()
