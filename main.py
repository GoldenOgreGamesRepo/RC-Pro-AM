import pygame
import sys
from car import Car
from settings import SCREEN_RES, GAME_BG, FPS, TRACKS

pygame.init()

screen = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("R.C. Python Game")
clock = pygame.time.Clock()

# Load track
current_track = TRACKS["track_1"]
track = pygame.image.load(current_track["image"]).convert()

# Load collision map
collision_map = pygame.image.load("track_1_collision.png").convert()

# Load car
start_x, start_y = current_track["start_pos"]
player_car = Car(start_x, start_y, "car_1.png")
player_car.angle = current_track["start_angle"]


# -------------------------------
# CAMERA
# -------------------------------
def get_camera_offset(player_pos):
    return pygame.Vector2(
        player_pos.x - SCREEN_RES[0] // 2,
        player_pos.y - SCREEN_RES[1] // 2
    )


# -------------------------------
# CIRCLE COLLISION
# -------------------------------
def circle_collision(car, collision_map):
    """Returns the collision normal if the circle touches a wall."""
    r = car.radius
    cx, cy = car.pos.x, car.pos.y

    # Sample 8 points around the circle
    for angle in range(0, 360, 45):
        offset = pygame.Vector2(r, 0).rotate(angle)
        px = int(cx + offset.x)
        py = int(cy + offset.y)

        if 0 <= px < collision_map.get_width() and 0 <= py < collision_map.get_height():
            if collision_map.get_at((px, py)) == (0, 0, 0, 255):
                # Normal = from wall pixel → car center
                normal = (car.pos - pygame.Vector2(px, py)).normalize()
                return normal

    return None
# -------------------------------
# CHECKOUNT
# -------------------------------
def check_checkpoint(car, track):
    if car.finished:
        return

    checkpoints = track["checkpoints"]
    radius = track["checkpoint_radius"]

    # Position of the next checkpoint
    target_x, target_y = checkpoints[car.next_checkpoint]
    dist = car.pos.distance_to(pygame.Vector2(target_x, target_y))

    if dist < radius:
        # Hit the correct checkpoint
        car.next_checkpoint += 1

        # If we hit the last checkpoint, we now expect checkpoint 0 (finish line)
        if car.next_checkpoint == len(checkpoints):
            car.next_checkpoint = 0
            car.ready_to_finish = True

        # If we hit checkpoint 0 AND we were ready to finish → lap complete
        elif car.next_checkpoint == 1 and car.ready_to_finish:
            car.current_lap += 1
            car.ready_to_finish = False

            if car.current_lap > track["laps"]:
                car.finished = True
                print("FINISHED!")


# -------------------------------
# GAME LOOP
# -------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GAME_BG)

    camera_offset = get_camera_offset(player_car.pos)
    screen.blit(track, (-camera_offset.x, -camera_offset.y))

    # Update physics
    player_car.update()
    # Checkpoint 
    check_checkpoint(player_car, current_track)
    # Move car
    player_car.pos += player_car.velocity

    # Check circle collision
    normal = circle_collision(player_car, collision_map)

    if normal:
        # Push car out of wall
        player_car.pos += normal * 2.5

        # Remove inward velocity
        inward = player_car.velocity.dot(normal)
        if inward > 0:
            player_car.velocity -= normal * inward

        # Add bounce
        player_car.velocity += normal * 0.6

        # Slow down
        player_car.velocity *= 0.82

        # Rotate away slightly
        player_car.angle += normal.x * 1.2
        player_car.angle -= normal.y * 1.2
    # Draw checkpoints
    for i, (x, y) in enumerate(current_track["checkpoints"]):
        color = (0, 255, 0) if i == player_car.next_checkpoint else (255, 255, 0)
        pygame.draw.circle(screen, color, (x - camera_offset.x, y - camera_offset.y), current_track["checkpoint_radius"], 2)

    # Draw car
    player_car.draw(screen, camera_offset)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
