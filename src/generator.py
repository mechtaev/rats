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
        colonies = [(0, AI()), (1, AI())]
        holes_for_colony = utils.partition(self.holes, len(colonies))
        self.colonies = []
        for index, (color, ai) in enumerate(colonies):
            holes = holes_for_colony[index]
            colony = Colony(color, ai, holes)
            for i in range(config.num_rats):
                colony.add_new_rat(self.randpoint(), random.choice(holes), 0)
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

    

        
