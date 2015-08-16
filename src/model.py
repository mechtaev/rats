import random
import utils
import collections
from faker import Factory

_fake = Factory.create('ru_RU')

Point = collections.namedtuple('Point', ['x', 'y'])

class Hole:

    def __init__(self, location):
        self.location = location

class Map:

    def __init__(self, num_food, num_holes):
        self.size = Point(800, 600)
                
        self.food = []
        for i in range(num_food):
            self.food.append(self.randpoint())

        self.holes = []
        for i in range(num_holes):
            self.holes.append(Hole(self.randpoint()))


    def randpoint(self):
        x = random.randint(0, self.size.x)
        y = random.randint(0, self.size.y)
        return Point(x, y)


class Assignment:

    def finished(self, rat, colony, model):
        return True

    def step(self, rat, colony, model):
        pass


class Rat:

    def __init__(self, location):
        self.location = location
        self.assignment = Assignment()
        self.name = _fake.name()

    def step(self, colony, model):
        self.assignment.step(self, colony, model)


class Colony:

    def __init__(self, ai, rats, holes):
        self.ai = ai
        self.rats = rats
        self.belongs = dict()
        rats_for_holes = utils.partition(rats, len(holes))
        for index, partition in enumerate(rats_for_holes):
            for rat in partition:
                self.belongs[rat] = holes[index]

    def step(self, model):
        self.ai.step(self, model)

    
class Model:

    def __init__(self, num_rats, num_food, num_holes, colonies_ais):

        self.map = Map(num_food, num_holes)

        holes_for_colony = utils.partition(self.map.holes, len(colonies_ais))

        self.colonies = []
        for index, ai in enumerate(colonies_ais):
            rats = []
            for i in range(num_rats):
                rats.append(Rat(self.map.randpoint()))
            
            colony = Colony(ai, rats, holes_for_colony[index])
            self.colonies.append(colony)

    def step(self):
        for colony in self.colonies:
            colony.step(self)
