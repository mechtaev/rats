import logging
from model import *
from assignments import Move


_logger = logging.getLogger(__name__)


class AI:

    def step(self, colony, model):
        for rat in colony.rats:
            if rat.assignment.finished(rat, colony, model):
                _logger.info("[{}] {} finished its assignment".format(str(model.time), rat.name))
                rat.assignment = Move(model.map.randpoint())
            rat.step(colony, model)
            
