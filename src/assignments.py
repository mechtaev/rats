from model import *
import random
import config
import utils
import math
import logging


_logger = logging.getLogger(__name__)


# Succeed if all succeed. If one fails, stop execution.
class Pipe(Assignment):

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


# Return status of the last assignment, don't require success to continue
class Seq(Assignment):

    def __init__(self, assignments):
        self.assignments = assignments
        self.current = assignments.pop(0)

    def step(self, rat, colony, model):
        if self.current.status(rat, colony, model) != Status.in_progress:
            if len(self.assignments) > 0:
                self.current = self.assignments.pop(0)
        else:
            self.current.step(rat, colony, model)

    def status(self, rat, colony, model):
        if len(self.assignments) == 0 and self.current.status(rat, colony, model) != Status.in_progress:
            return self.current.status(rat, colony, model)
        return Status.in_progress


class TakeFood(Assignment):

    def __init__(self):
        self.tried = False
        self.taken = False

    def step(self, rat, colony, model):
        self.tried = True
        result = next((i for (i, r) in enumerate(model.map.food) if r.topleft == rat.rect.topleft), None)
        if result is None:
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


class Fight(Assignment):

    def __init__(self, enemy, hostile_colony):
        self.enemy = enemy
        self.hostile_colony = hostile_colony
        self.finished = False

    def step(self, rat, colony, model):
        kill = random.randint(0, config.kill_probability) == 0
        if kill:
            dead = self.hostile_colony.kill_rat(self.enemy, model.time)
            if dead is not None:
                model.map.dead_bodies.append(dead)
            self.finished = True

    def status(self, rat, colony, model):
        if self.finished:
            return Status.success
        else:
            return Status.in_progress


class Move(Assignment):

    def __init__(self, destination, conscious):
        self.conscious = conscious
        self.destination = destination

    def find_enemy(self, rat, colony, model):
        for other_colony in model.colonies:
            if other_colony == colony:
                continue
            else:
                for enemy in other_colony.get_rats():
                    dsq = utils.distance_square(enemy.rect.topleft, rat.rect.topleft)
                    if dsq <= config.sight_distance ** 2:
                        dist = int(math.sqrt(dsq))
                        return (enemy, other_colony, dist)
        return None

    def step(self, rat, colony, model):
        if self.conscious:
            target = self.find_enemy(rat, colony, model)
            if target is not None:
                enemy, hostile_colony, dist = target
                assignments = []
                if dist <= config.attack_distance:
                    assignments.append(Fight(enemy, hostile_colony))
                else:
                    move = Move(utils.middlepoint(enemy.rect.topleft, rat.rect.topleft), False)
                    assignments.append(move)
                assignments.append(rat.assignment)
                rat.assignment = Seq(assignments)
                return
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
