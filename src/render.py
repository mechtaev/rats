import pygame
import os
import config
import logging


_logger = logging.getLogger(__name__)


class View:

    def __init__(self, size):
        self.size = size

        self.images = dict()
        self.images['rat'] = dict()
        self.images['rat_moving'] = dict()
        self.images['rat'][0] = pygame.image.load(os.path.join('data', 'rat.png'))
        self.images['rat_moving'][0] = pygame.image.load(os.path.join('data', 'rat_moving.png'))
        self.images['rat'][1] = pygame.image.load(os.path.join('data', 'white_rat.png'))
        self.images['rat_moving'][1] = pygame.image.load(os.path.join('data', 'white_rat_moving.png'))
        self.images['food'] = pygame.image.load(os.path.join('data', 'food.png'))
        self.images['hole'] = pygame.image.load(os.path.join('data', 'hole.png'))

        self.font = pygame.font.SysFont(config.font_name, config.font_size)

        if config.fullscreen:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Rats " + str(config.version))

    def render(self, model):
        self.screen.fill(config.background)

        for hole in model.map.holes:
            self._render_hole(hole)
        for food in model.map.food:
            self.screen.blit(self.images['food'], food)
        for dead in model.map.dead_bodies:
            self._render_dead(dead)
        for colony in model.colonies:
            for rat in colony.get_rats():
                if not rat.invisible:
                    self._render_rat(rat)

        self._render_info(model)

        pygame.display.flip()

    def _render_hole(self, hole):
        self.screen.blit(self.images['hole'], hole.rect)
        label = self.font.render(str(hole.food), True, config.foreground)
        self.screen.blit(label, (hole.rect.topright[0] + 5, hole.rect.topright[1] - 5))

    def _render_rat(self, rat):
        if config.show_names:
            label = self.font.render(rat.name, True, config.foreground)
            self.screen.blit(label, (rat.rect.topright[0] + 5, rat.rect.topright[1] - 10))
        if rat.movement_phase < (config.movement_cycle / 2):
            baseimage = self.images['rat'][rat.color]
        else:
            baseimage = self.images['rat_moving'][rat.color]
        if rat.look_left:
            image = baseimage
        else:
            image = pygame.transform.flip(baseimage, True, False)
        self.screen.blit(image, rat.rect)
        if rat.carry_food:
            if rat.look_left:
                point = (rat.rect.topleft[0] - 4, rat.rect.topleft[1] + 3)
                rect = pygame.Rect(point, config.food_size)
            else:
                point = (rat.rect.topright[0] - 2, rat.rect.topright[1] + 3)
                rect = pygame.Rect(point, config.food_size)
            self.screen.blit(self.images['food'], rect)

    def _render_dead(self, rat):
        if config.show_names:
            label = self.font.render(rat.name, True, config.foreground)
            self.screen.blit(label, (rat.rect.topright[0] + 5, rat.rect.topright[1] - 10))
        baseimage = pygame.transform.flip(self.images['rat'][rat.color], False, True)
        if rat.look_left:
            image = baseimage
        else:
            image = pygame.transform.flip(baseimage, True, False)
        self.screen.blit(image, rat.rect)

    def _render_info(self, model):
        label_time = self.font.render("Time", True, config.foreground)
        label_time_value = self.font.render(str(model.time), True, config.foreground)
        label_food = self.font.render("Food", True, config.foreground)
        label_food_value = self.font.render(str(len(model.map.food)), True, config.foreground)
        label_help = self.font.render("Press Q to quit", True, config.foreground)

        label_rats = self.font.render("Rats", True, config.foreground)
        labels_rats_value = []
        colonies = sorted(model.colonies, key=(lambda c: len(c.get_rats())), reverse=True)
        for colony in colonies:
            rats_num = str(len(colony.get_rats()))
            label_rats_value = self.font.render(rats_num, True, config.color[colony.color])
            labels_rats_value.append(label_rats_value)

        x_offset = 15
        y_offset = 15
        x_offset_right = 90
        y_offset_right = 15
        x_value_offset = 50
        y_increment = 15
        self.screen.blit(label_time, (x_offset, y_offset))
        self.screen.blit(label_time_value, (x_value_offset, y_offset))
        y_offset = y_offset + y_increment
        self.screen.blit(label_food, (x_offset, y_offset))
        self.screen.blit(label_food_value, (x_value_offset, y_offset))
        y_offset = y_offset + y_increment
        self.screen.blit(label_rats, (x_offset, y_offset))
        for label in labels_rats_value:
            self.screen.blit(label, (x_value_offset, y_offset))
            y_offset = y_offset + y_increment
        self.screen.blit(label_help, (self.size[0] - x_offset_right, y_offset_right))
