import pygame
import sys
from car import Car
from settings import SCREEN_RES, GAME_BG, FPS, TRACKS

pygame.init()

screen = pygame.display.set_mode(SCREEN_RES)  
pygame.display.set_caption("R.C. Python Game")
clock = pygame.time.Clock()
# Load Car and Track
start_x, start_y = TRACKS["track_1"]["start_pos"] 
player_car = Car(start_x, start_y, "car_1.png") 
player_car.angle = TRACKS["track_1"]["start_angle"]
current_track = TRACKS["track_1"]
track = pygame.image.load(current_track["image"]).convert()
track_rect = track.get_rect()

# Camera Function
def get_camera_offset(player_pos):
    # Center camera on player
    offset_x = player_pos.x - SCREEN_RES[0] // 2
    offset_y = player_pos.y - SCREEN_RES[1] // 2
    return pygame.Vector2(offset_x, offset_y)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(GAME_BG)
    camera_offset = get_camera_offset(player_car.pos) # Draw track 
    screen.blit(track, (-camera_offset.x, -camera_offset.y))
    
    player_car.update()
    player_car.draw(screen, camera_offset)

    pygame.display.flip()
    clock.tick(FPS) 

# Quit Pygame
pygame.quit()
sys.exit()