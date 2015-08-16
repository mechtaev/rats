import pygame
import os


pygame.init()

images = dict()
images['rat']  = pygame.image.load(os.path.join('data', 'rat.png'))
images['food'] = pygame.image.load(os.path.join('data', 'food.png'))
images['hole'] = pygame.image.load(os.path.join('data', 'hole.png'))

background = (200, 255, 200)


class View:

    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)

    def render(self, model):
        self.screen.fill(background)
        for hole in model.map.holes:
            self.screen.blit(images['hole'], hole.rect)
        for food in model.map.food:
            self.screen.blit(images['food'], food)
        for colony in model.colonies:
            for rat in colony.rats:
                if rat.look_left:
                    image = images['rat']
                else:
                    image = pygame.transform.flip(images['rat'], True, False)                    
                self.screen.blit(image, rat.rect)
        pygame.display.flip()
