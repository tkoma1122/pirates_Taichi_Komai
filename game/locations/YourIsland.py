from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

class YourIsland(location.Location):

    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "island"
        self.symbol = 'Y'
        self.visitable = True
        self.starting_location = BeachWithShip(self)
        self.Fairy_Forest = FairyForest(self)
        self.current_location = self.starting_location
        self.locations = {}
        self.locations["FairyIsland"] = self.Fairy_Forest
        self.locations["southBeach"] = self.starting_location
        self.locations["shrine"] = Shrine(self)

    def enter(self, ship):
        announce("You arrive at an island.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

    def move(self, direction):
        next_location = self.current_location.get_next_location(direction)
        if next_location:
            self.current_location = next_location
            self.current_location.enter()
        else:
            announce("You can't go that way.")

class BeachWithShip(location.SubLocation):

    def enter(self):
        announce("You arrived the Mythic Island.")

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name ="southBeach"
        self.verbs["north"] = self
        self.verbs["south"] = self

    def process_verb(self, verb, cmd_list, nouns):
        if(verb == "north"):
            config.the_player.next_loc = self.main_location.locations["shrine"]
        if(verb == "south"):
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False

    def get_next_location(self, direction):
        if direction == "north":
            return self.main_location.locations["shrine"]
        elif direction == "south":
            return config.the_player.ship  # Assuming this is the ship location
        else:
            return None

class Shrine(location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name ="shrine"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["investigate"] = self

        self.shrineUsed = False
        self.RidDLE_AMOUNT = 3

    def enter(self):
        announce("You walk to the top of the hill. A finely-crafted shrine sits before you. You can investigate the shrine.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "investigate":
            self.handle_shrine()

    def handle_shrine(self):
        if not self.shrineUsed:
            announce("You investigate the shrine and hear a voice in your head.")
            announce("'I am the guardian of this shrine. Answer my riddles and be rewarded.'")
            choice = input("Answer the riddles? ")

            if "yes" in choice.lower():
                self.handle_riddles()
            else:
                announce("You turn away from the shrine.")
        else:
            announce("The shrine lies dormant.")

    def handle_riddles(self):
        riddle = self.get_riddle_and_answer()
        guesses = self.RidDLE_AMOUNT
        self.shrineUsed = True

        while guesses > 0:
            announce(riddle[0])
            plural = "" if guesses == 1 else "s"
            announce(f"You have {guesses} attempt{plural} left.")
            choice = input("What is your guess? ")

            if riddle[1] in choice.lower():
                self.riddle_reward()
                announce("You have guessed correctly and received the SwordofJustice!")
                config.the_player.add_item(SwordofJustice())
                break
            else:
                guesses -= 1
                announce("You have guessed incorrectly.")

    def RiddleReward(self):
        for i in config.the_player.get_pirates():
            i.health = i.max_health

    def GetRiddleAndAnswer(self):
        riddleList = [("Under a full moon, I throw a yellow hat into the red sea. What happens to the yellow hat??", "wet")]
        return random.choice(riddleList)
    
    def get_next_location(self, direction):
        if direction in ["north", "east", "south", "west"]:
            return self.main_location.locations["southBeach"]
        else:
            return None
    
class FairyForest(location.SubLocation):
    def enter(self):
        announce("You've arrived at the Fairy Forest. To obtain a powerful treasure, solve the Number Puzzle Game.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "play":
            self.play_number_puzzle()

    def play_number_puzzle(self):
        target_number = random.randint(1, 100)
        announce(f"Find the number! It's between 1 and 100.")

        while True:
            guess = int(input("Enter your guess: "))
            if guess < target_number:
                announce("Go higher.")
            elif guess > target_number:
                announce("Go lower.")
            else:
                announce("Congratulations! You've solved the puzzle and obtained the MythicBowGun.")
                config.the_player.add_item(MythicBowGun())
                break

def handle_movement(player_input):
    directions = ["north", "south", "east", "west"]
    if player_input in directions:
        YourIsland.current_location.move(player_input)
    else:
        announce("Invalid direction. Try 'north', 'south', 'east', or 'west'.")

player_input = input("Enter a direction to move: ")
handle_movement(player_input)

class MythicBowGun(Item):
    def __init__(self):
        super().__init__("MythicBowGun", 1)
        self.damage = (40,400)
        self.charges = 2
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"

class SwordofJustice(Item):
    def __init__(self):
        super().__init__("SwordofJustice", 1)
        self.damage = (50,500)
        self.skill = "swords"
        self.verb = "attack"
        self.verb2 = "attacks"







         