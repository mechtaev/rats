from model import *
import random
import config


_logger = logging.getLogger(__name__)


class Compound(Assignment):

    def __init__(self, assignments):
        self.assignments = assignments
        self.current = assignments.pop(0)
        self.success = True

    def step(self, rat, colony, model):
        if not self.success:
            pass
        elif self.current.status(rat, colony, model) == Status.success:
            if len(self.assignments) > 0:
                self.current = self.assignments.pop(0)
        elif self.current.status(rat, colony, model) == Status.failure:
            self.success = False
        else:
            self.current.step(rat, colony, model)

    def status(self, rat, colony, model):
        if not self.success:
            return Status.failure
        if self.current.status(rat, colony, model) == Status.failure:
            return Status.failure
        if len(self.assignments) == 0 and self.current.status(rat, colony, model) == Status.success:
            return Status.success
        return Status.in_progress


class TakeFood(Assignment):

    def __init__(self):
        self.tried = False
        self.taken = False

    def step(self, rat, colony, model):
        self.tried = True
        result = next((i for (i, r) in enumerate(model.map.food) if r.topleft == rat.rect.topleft), None)
        if result == None:
            self.taken = False
        else:
            self.taken = True
            rat.carry_food = True
            del model.map.food[result]        

    def status(self, rat, colony, model):
        if not self.tried:
            return Status.in_progress
        if self.tried and not self.taken:
            return Status.failure
        return Status.success


class PutFood(Assignment):

    def __init__(self):
        self.put = False

    def step(self, rat, colony, model):
        if not self.put:
            self.put = True
            hole = colony.belongs[rat]
            hole.food = hole.food + config.cheese_weigth
            rat.carry_food = False

    def status(self, rat, colony, model):
        if self.put:
            return Status.success
        else:
            return Status.in_progress


class Invisible(Assignment):

    def __init__(self, period):
        self.period = period
        self.appeared = False
        self.first_time = True

    def step(self, rat, colony, model):
        if self.first_time:
            self.start_time = model.time
            self.first_time = False
        if model.time - self.start_time <= self.period:
            rat.invisible = True
        else:
            rat.invisible = False
            self.appeared = True

    def status(self, rat, colony, model):
        if self.appeared:
            return Status.success
        else:
            return Status.in_progress


class Move(Assignment):

    def __init__(self, destination):
        self.destination = destination

    def step(self, rat, colony, model):
        possible_moves = []
        if rat.rect.topleft == self.destination:
            return
        dx = self.destination[0] - rat.rect.x
        dy = self.destination[1] - rat.rect.y
        result = random.randint(0, abs(dx) + abs(dy) + min(abs(dx), abs(dy) - 1))
        if result < abs(dx):
            if dx > 0:
                move = (1, 0)
            else:
                move = (-1, 0)
        elif result >= abs(dx) and result < abs(dx) + abs(dy):
            if dy > 0:
                move = (0, 1)
            else:
                move = (0, -1)
        else:
            if dx >= 0 and dy >= 0:
                move = (1, 1)
            elif dx >= 0 and dy < 0:
                move = (1, -1)
            elif dx < 0 and dy >= 0:
                move = (-1, 1)
            else:
                move = (-1, -1)
        if rat.look_left and move[0] > 0:
            rat.look_left = False
        if (not rat.look_left) and move[0] < 0:
            rat.look_left = True
        rat.movement_phase = (rat.movement_phase + 1) % config.movement_cycle
        rat.rect.move_ip(move)

    def status(self, rat, colony, model):
        if rat.rect.topleft == self.destination:
            return Status.success
        else:
            return Status.in_progress
