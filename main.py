import pygame
import sys

# Initialize Pygame
pygame.init()
# Set up display
SCREEN_RES = (800, 600)
screen = pygame.display.set_mode(SCREEN_RES)  
pygame.display.set_caption("R.C. Python Game")
clock = pygame.time.Clock()

GAME_BG = (30, 120, 30)  # Green background



# Player Car setup
car_pos = pygame.Vector2(SCREEN_RES[0] // 2, SCREEN_RES[1] // 2)
car_angle = 0
car_speed = 0
car_surface = pygame.Surface((40, 20)) # W and H of the car
car_surface = pygame.image.load("car_1.png").convert_alpha()




# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Handle key presses for car control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_angle += 3  # Accelerate
    elif keys[pygame.K_RIGHT]:
        car_angle -= 3  # Decelerate
    
    # Forward movement
    if keys[pygame.K_UP] :
        car_speed = 4
    elif keys[pygame.K_DOWN] :
        car_speed = -2
    else:
        car_speed = 0

    # Move the car
    direction = pygame.Vector2(1, 0).rotate(-car_angle)  # Get the direction vector based on the angle
    car_pos += direction * car_speed  # Move the car in the direction it's facing

    # Fill the background
    screen.fill(GAME_BG)  # White background

    # Rotate the car surface and get the new rect
    rotated_car = pygame.transform.rotate(car_surface, car_angle)
    car_rect = rotated_car.get_rect(center=car_pos)
    # Draw the car
    screen.blit(rotated_car, car_rect.topleft)

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

# Quit Pygame
pygame.quit()
sys.exit()