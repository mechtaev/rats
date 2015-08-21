import logging
import random
from model import *
from assignments import *
import utils


_logger = logging.getLogger(__name__)


class AI:

    def step(self, colony, model):
        for rat in colony.get_rats():
            if rat.assignment.status(rat, colony, model) != Status.in_progress:
                if len(model.map.food) > 0:
                    rat.assignment = self.find_food(rat, colony, model)
            rat.step(colony, model)

    def find_food(self, rat, colony, model):
        assignments = []

        def distance_from_rat(rect):
            return utils.distance_square(rat.rect.topleft, rect.topleft)

        destination = random.choice(sorted(model.map.food, key=distance_from_rat)[:3]).topleft
        assignments.append(Move(destination, True))
        assignments.append(TakeFood())
        assignments.append(Move(colony.belongs[rat].rect.topleft, True))
        assignments.append(PutFood())
        assignments.append(Invisible(config.in_hole_period))
        return Pipe(assignments)
