import pygame
import os
import model
import config

pygame.init()

images = dict()
images['rat'] = pygame.image.load(os.path.join('data', 'rat.png'))
images['rat_moving'] = pygame.image.load(os.path.join('data', 'rat_moving.png'))
images['white_rat'] = pygame.image.load(os.path.join('data', 'white_rat.png'))
images['white_rat_moving'] = pygame.image.load(os.path.join('data', 'white_rat_moving.png'))
images['food'] = pygame.image.load(os.path.join('data', 'food.png'))
images['hole'] = pygame.image.load(os.path.join('data', 'hole.png'))

font = pygame.font.SysFont(config.font_name, config.font_size)

class View:

    def __init__(self, size):
        if config.fullscreen:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)

    def render(self, model):
        self.screen.fill(config.background)
        
        for hole in model.map.holes:
            self._render_hole(hole)
        for food in model.map.food:
            self.screen.blit(images['food'], food)
        for dead in model.map.dead_bodies:
            self._render_dead(dead)
        for colony in model.colonies:
            for rat in colony.rats:
                if not rat.invisible:
                    self._render_rat(rat)

        label_time = font.render("Time: " + str(model.time), True, config.foreground)
        label_rats = font.render("Rats: " + str(len(model.colonies[0].rats)), True, config.foreground)
        label_food = font.render("Food: " + str(len(model.map.food)), True, config.foreground)

        self.screen.blit(label_time, (10, 10))
        self.screen.blit(label_rats, (10, 20))
        self.screen.blit(label_food, (10, 30))

        pygame.display.flip()

    def _render_hole(self, hole):
        self.screen.blit(images['hole'], hole.rect)
        label = font.render(str(hole.food), True, config.foreground)
        self.screen.blit(label, (hole.rect.topright[0] + 5, hole.rect.topright[1] - 5))

    def _render_rat(self, rat):
        if config.show_names:
            label = font.render(rat.name, True, config.foreground)
            self.screen.blit(label, (rat.rect.topright[0] + 5, rat.rect.topright[1] - 10))
        if rat.movement_phase < (config.movement_cycle / 2):
            if rat.color == 0:
                baseimage = images['rat']
            else:
                baseimage = images['white_rat']
        else:
            if rat.color == 0:
                baseimage = images['rat_moving']
            else:
                baseimage = images['white_rat_moving']
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
            self.screen.blit(images['food'], rect)

    def _render_dead(self, rat):
        if config.show_names:
            label = font.render(rat.name, True, config.foreground)
            self.screen.blit(label, (rat.rect.topright[0] + 5, rat.rect.topright[1] - 10))
        if rat.color == 0:
            baseimage = pygame.transform.flip(images['rat'], False, True)
        else:
            baseimage = pygame.transform.flip(images['white_rat'], False, True)
        if rat.look_left:
            image = baseimage
        else:
            image = pygame.transform.flip(baseimage, True, False)
        self.screen.blit(image, rat.rect)
