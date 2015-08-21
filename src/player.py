import logging
import utils
import config


_logger = logging.getLogger(__name__)


class Player:

    def __init__(self):
        self.last_click = None

    def step(self, colony, model):
        if self.last_click is not None:
            for hole in model.map.holes:
                if utils.distance_square(self.last_click, hole.rect.topleft) <= config.click_radius**2:
                    if not (hole in colony.get_holes()):
                        if hole in colony.targets:
                            colony.targets.remove(hole)
                        else:
                            colony.targets.append(hole)
            self.last_click = None

    def process_click(self, pos):
        self.last_click = pos
