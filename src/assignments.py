from model import *
import random

class Move(Assignment):

    def __init__(self, destination):
        self.destination = destination

    def step(self, rat, colony, model):
        possible_moves = []
        if rat.location == self.destination:
            return
        if rat.location.x > self.destination.x:
            possible_moves.append(Point(1, 0))
        if rat.location.x < self.destination.x:
            possible_moves.append(Point(-1, 0))
        if rat.location.y > self.destination.y:
            possible_moves.append(Point(0, 1))
        if rat.location.y < self.destination.y:
            possible_moves.append(Point(0, -1))
        if rat.location.x > self.destination.x and rat.location.y > self.destination.y:
            possible_moves.append(Point(1, 1))
        if rat.location.x < self.destination.x and rat.location.y < self.destination.y:
            possible_moves.append(Point(-1, -1))
                
        move = random.choice(possible_moves)

        rat.location = Point(rat.location.x + move.x, rat.location.y + move.y)


    def finished(self, rat, colony, model):
        return rat.location == self.destination
