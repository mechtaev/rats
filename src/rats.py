import config
import pygame
import model
import render
from generator import Generator
import logging
from player import Player
from computer import Computer
import menu
from time import time, sleep
import globals


if __name__ == "__main__":

    logging.basicConfig(filename='rats.log', level=logging.INFO)

    if config.enable_menu:
        menu.show_menu()

    pygame.init()
    player = Player()
    generator = Generator(player)
    game = model.Model(generator)
    view = render.View(game.map.size)
    measure_time_period = 20
    measure_time_phase = 0
    speed = config.initial_speed
    running = True
    while running:
        if measure_time_phase == 0:
            total_time = 0.0
            game_time = 0.0
        measure_time_phase = (measure_time_phase + 1) % measure_time_period
        start_time = time()
        game.step()
        view.render(game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                player.process_click(pos)
        game_time = game_time + (time() - start_time)
        sleep(speed)
        total_time = total_time + (time() - start_time)
        if measure_time_phase == 0:
            globals.fps = int(measure_time_period / total_time)
            extected = config.speed_value[config.speed] * config.normal_fps
            if speed < 0.001:
                speed = 0.001
            else:
                speed = speed * (globals.fps / extected)
            globals.max_fps = int(measure_time_period / game_time)
