import utils
import random
from model import *
import pygame
from ai import AI

class Generator:

    def __init__(self):
        if config.fullscreen:
            infoObject = pygame.display.Info()
            self.map_size = (infoObject.current_w, infoObject.current_h)
        else:
            self.map_size = config.size
        self.holes = []
        for i in range(config.num_holes):
            self.holes.append(Hole(self.randpoint())) # should be less random
        colonies_ais = [AI()]
        holes_for_colony = utils.partition(self.holes, len(colonies_ais))
        self.colonies = []
        for index, ai in enumerate(colonies_ais):
            rats = []
            for i in range(config.num_rats):
                rats.append(Rat(random.choice([0, 1]), self.randpoint(), 0)) # should be less random
            colony = Colony(ai, rats, holes_for_colony[index])
            self.colonies.append(colony)

    def randpoint(self):
        x = random.randint(0, self.map_size[0])
        y = random.randint(0, self.map_size[1])
        return (x, y)

    def initial_food(self):
        food = []
        for i in range(config.num_food):
            food.append(self.new_food())
        return food

    def new_food(self):
        return pygame.Rect(self.randpoint(), config.food_size)

    

        
