import pygame
import sys
from car import Car
from settings import SCREEN_RES, GAME_BG, FPS

pygame.init()

screen = pygame.display.set_mode(SCREEN_RES)  
pygame.display.set_caption("R.C. Python Game")
clock = pygame.time.Clock()

player_car = Car(SCREEN_RES[0] // 2, SCREEN_RES[1] // 2, "car_1.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(GAME_BG)

    player_car.update()
    player_car.draw(screen)

    pygame.display.flip()
    clock.tick(FPS) 

# Quit Pygame
pygame.quit()
sys.exit()