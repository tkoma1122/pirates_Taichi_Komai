from game import location
from game.config import config
from game.display import announce
from game.items import Item
import random

class YourIsland(location.Location):

    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "island"
        self.symbol = 'Y'
        self.visitable = True
        self.starting_location = BeachWithShip(self)
        self.Fairy_Forest = FairyForest(self)
        
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

class BeachWithShip(location.SubLocation):

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
        if(verb == "north" or verb == "east" or verb == "south" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if(verb == "investigate"):
            self.HandleShrine()

    def HandleShrine(self):
        if (not self.shrineUsed):
            announce("You investigate the shrine and hear a voice in your head.")
            announce("'I am the guardian of this shrine. Answer my riddles and be rewarded.'")
            choice = input("Answer the riddles?")
            if ("yes" in choice.lower()):
                self.HandleRiddles()
            else:
                announce("You turn away from the shrine.")
        else:
            announce("The shrine lays dormant.")

    def HandleRiddles(self):
        riddle = self.GetRiddleAndAnswer()
        guesses = self.RidDLE_AMOUNT
        self.shrineUsed = True

        while (guesses > 0):

            print(riddle[0])
            plural = ""
            if(guesses != 1):
                plural = "s"

            print(f"You have {guesses} left.")
            choice = input("What is your guess?")

            if (riddle[1] in choice.lower()):
                self.RiddleReward()
                announce('You have guessed correctly and been blessed by the spirit.')
                guesses = 0
            else:
                guesses -= 1
                announce("You have guessed incorrectly.")

    def RiddleReward(self):
        for i in config.the_player.get_pirates():
            i.health = i.max_health

    def GetRiddleAndAnswer(self):
        riddleList = [("Under a full moon, I throw a yellow hat into the red sea. What happens to the yellow hat??", "wet")]
        return random.choice(riddleList)
    
class FairyForest(location.SubLocation):
    def enter(self):
        announce("You arrived the Fairy Forest. To get powerful treasure, you should solve Puzzle Game.")

    def process_verb(self, verb, cmd_list, nouns):
        pass


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







         