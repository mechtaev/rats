from model import *
from assignments import Move

class AI:

    def step(self, colony, model):

        for rat in colony.rats:
            if rat.assignment.finished(rat, colony, model):
                rat.assignment = Move(model.map.randpoint())
            rat.step(colony, model)
            
