import random
import logging
import config
from enum import Enum
from pygame import Rect
from faker import Factory
import quadtree


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

    # Without index it gives me 25 max-fps with 100 rats in a colony in fullscreen mode
    # With index, it is about 50
    # this is a stupid solution (I need to update it each step of each colony)
    def update_enemy_index(self, colony, model):
        rats = []
        for other_colony in model.colonies:
            if other_colony == colony:
                continue
            else:
                rats += other_colony.get_rats()
        if len(rats) > 0:
            self.index = quadtree.QuadTree(rats, 5) # magic number
        else:
            self.index = None

    def get_neighbours(self, rat, distance):
        if self.index is None:
            return []
        box = Rect(rat.left - distance,
                   rat.top - distance,
                   2 * distance,
                   2 * distance)
        return self.index.hit(box)


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

    @property
    def rect(self):
        return self._rect

    # it is already not nice. I should somehow ingrate them with rect better
    @rect.setter
    def rect(self, value):
        self.left = value.left
        self.right = value.left
        self.top = value.top
        self.bottom = value.top
        self._rect = value

    def __init__(self, color, name, location, birthtime):
        self.color = color
        self.rect = Rect(location, config.rat_size)
        self.assignment = Assignment()
        self.look_left = True
        self.movement_phase = 0
        self.name = name
        self.carry_food = False
        self.last_eat = birthtime
        self.invisible = False

    def step(self, colony, model):
        self.assignment.step(self, colony, model)


class Colony:

    def __init__(self, color, holes, manager, player):
        self.color = color
        self._fake = Factory.create(config.locale[color])
        self.manager = manager
        self.player = player
        self._rats = []
        self._holes = holes
        self.belongs = dict()
        self.targets = []

    def step(self, model):
        # eating
        for rat in self._rats:
            if model.time - rat.last_eat >= config.eating_period:
                hole = self.belongs[rat]
                if hole.food == 0:
                    dead = self.kill_rat(rat, model.time)
                    if dead is not None:
                        model.map.dead_bodies.append(dead)
                else:
                    hole.food = hole.food - 1
                    rat.last_eat = model.time
        # creating new rats
        if model.time % config.birth_period == 0:
            for hole in self._holes:
                if hole.food >= config.birth_threshold:
                    self.add_new_rat(hole.rect.topleft, hole, model.time)
                    hole.food = hole.food - config.birth_price
        # updating index
        if config.use_index:
            model.map.update_enemy_index(self, model)
        # assignments
        self.manager.step(self, model)
        # decisions
        self.player.step(self, model)

    def kill_rat(self, rat, current_time):
        if rat in self._rats:
            self._rats.remove(rat)
            del self.belongs[rat]
            return DeadBody(rat, current_time)
        return None

    def add_new_rat(self, location, hole, current_time):
        newrat = Rat(self.color, self._fake.first_name(), location, current_time)
        self._rats.append(newrat)
        self.belongs[newrat] = hole

    def get_rats(self):
        return self._rats

    def get_holes(self):
        return self._holes


class Model:

    def __init__(self, generator):
        self.time = 0
        self.map = Map(generator)
        self.colonies = generator.colonies

    def step(self):
        self.time = self.time + 1
        if self.time % config.new_food_period_value[config.new_food_period] == 0:
            self.map.add_food()
        for dead_body in self.map.dead_bodies:
            if self.time - dead_body.time >= config.dead_body_period:
                self.map.dead_bodies.remove(dead_body)
        colonies_copy = self.colonies[:]
        random.shuffle(colonies_copy)
        for colony in colonies_copy:
            colony.step(self)
