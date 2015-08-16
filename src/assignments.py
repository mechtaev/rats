from model import *
import random


_logger = logging.getLogger(__name__)


class Move(Assignment):

    def __init__(self, destination):
        self.destination = destination

    def step(self, rat, colony, model):
        possible_moves = []
        if rat.rect.topleft == self.destination:
            return
        if rat.rect.x < self.destination[0]:
            possible_moves.append((1, 0))
        if rat.rect.x > self.destination[0]:
            possible_moves.append((-1, 0))
        if rat.rect.y < self.destination[1]:
            possible_moves.append((0, 1))
        if rat.rect.y > self.destination[1]:
            possible_moves.append((0, -1))
        if rat.rect.x < self.destination[0] and rat.rect.y < self.destination[1]:
            possible_moves.append((1, 1))
        if rat.rect.x > self.destination[0] and rat.rect.y > self.destination[1]:
            possible_moves.append((-1, -1))
        move = random.choice(possible_moves)
        if rat.look_left and move[0] > 0:
            rat.look_left = False
        if (not rat.look_left) and move[0] < 0:
            rat.look_left = True
        rat.rect.move_ip(move)


    def finished(self, rat, colony, model):
        return rat.rect.topleft == self.destination
