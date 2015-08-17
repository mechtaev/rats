import random
import utils
import collections
import logging
import config
from enum import Enum
from pygame import Rect
from faker import Factory


_fake = Factory.create('ru_RU')
_logger = logging.getLogger(__name__)


class Hole:

    def __init__(self, location):
        self.rect = Rect(location, config.hole_size)
        self.food = 0


class DeadBody:

    def __init__(self, rat, time):
        self.color = rat.color
        self.name = rat.name
        self.rect = rat.rect
        self.look_left = rat.look_left
        self.time = time

        
class Map:

    def __init__(self, generator):
        self._generator = generator
        self.size = generator.map_size
        self.food = generator.initial_food()
        self.holes = generator.holes
        self.dead_bodies = []

    def add_food(self):
        self.food.append(self._generator.new_food())


class Status(Enum):
    success = 1
    failure = 2
    in_progress = 3


class Assignment:

    def status(self, rat, colony, model):
        return Status.success

    def step(self, rat, colony, model):
        pass
    

class Rat:

    def __init__(self, color, location, birthtime):
        self.color = color
        self.rect = Rect(location, config.rat_size)
        self.assignment = Assignment()
        self.look_left = True
        self.movement_phase = 0
        self.name = _fake.first_name()
        self.carry_food = False
        self.last_eat = birthtime
        self.invisible = False

    def step(self, colony, model):
        self.assignment.step(self, colony, model)


class Colony:

    def __init__(self, ai, rats, holes):
        self.ai = ai
        self.rats = rats
        self.holes = holes
        self.belongs = dict()
        rats_for_holes = utils.partition(rats, len(holes))
        for index, partition in enumerate(rats_for_holes):
            for rat in partition:
                self.belongs[rat] = holes[index]

    def step(self, model):
        self.ai.step(self, model)

    
class Model:

    def __init__(self, generator):
        self.time = 0
        self.map = Map(generator)
        self.colonies = generator.colonies

    def step(self):
        self.time = self.time + 1
        if self.time % config.new_food_period == 0:
            self.map.add_food()
        for dead_body in self.map.dead_bodies:
            if self.time - dead_body.time >= config.dead_body_period:
                self.map.dead_bodies.remove(dead_body)
        for colony in self.colonies:
            if self.time % config.birth_period == 0:
                for hole in colony.holes:
                    if hole.food >= config.birth_threshold:
                        newrat = Rat(random.choice([0, 1]), hole.rect.topleft, self.time)
                        colony.rats.append(newrat)
                        colony.belongs[newrat] = hole
                        hole.food = hole.food - config.birth_price
            for rat in colony.rats:
                if self.time - rat.last_eat >= config.eating_period:
                    hole = colony.belongs[rat]
                    if hole.food == 0:
                        colony.rats.remove(rat)
                        del colony.belongs[rat]
                        self.map.dead_bodies.append(DeadBody(rat, self.time))
                    else:
                        hole.food = hole.food - 1
                        rat.last_eat = self.time
            colony.step(self)
