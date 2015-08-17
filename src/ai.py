import logging
import random
from model import *
from assignments import *


_logger = logging.getLogger(__name__)


class AI:

    def step(self, colony, model):
        for rat in colony.rats:
            if rat.assignment.status(rat, colony, model) != Status.in_progress:
                _logger.info("[{}] {} finished its assignment".format(str(model.time), rat.name))
                if len(model.map.food) > 0:
                    rat.assignment = self.find_food(rat, colony, model)
            rat.step(colony, model)

    def find_food(self, rat, colony, model):
        assignments = []
        def distance_from_rat(rect):
            return (rat.rect.x - rect.x)**2 + (rat.rect.y - rect.y)**2
        destination = random.choice(sorted(model.map.food, key=distance_from_rat)[:3]).topleft
        assignments.append(Move(destination))
        assignments.append(TakeFood())
        assignments.append(Move(colony.belongs[rat].rect.topleft))
        assignments.append(PutFood())
        assignments.append(Invisible(config.in_hole_period))
        return Compound(assignments)
