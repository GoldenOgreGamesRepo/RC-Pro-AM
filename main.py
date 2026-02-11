import pygame
import sys
from car import Car
from settings import SCREEN_RES, GAME_BG, FPS, TRACKS

pygame.init()

# HUD Display
font = pygame.font.Font(None, 36)

# Screen Setup
screen = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("R.C. Python Game")
clock = pygame.time.Clock()

# Load track
current_track = TRACKS["track_1"]
track = pygame.image.load(current_track["image"]).convert()

# Load collision map
collision_map = pygame.image.load(current_track["collision"]).convert()

# Load car
start_x, start_y = current_track["start_pos"]
player_car = Car(start_x, start_y, "car_1.png")
player_car.angle = current_track["start_angle"]


# -------------------------------
# HUD Drawing
# -------------------------------
def draw_text_with_shadow(text, x, y, color=(255,255,255)):
    shadow = font.render(text, True, (0, 0, 0))
    screen.blit(shadow, (x + 2, y + 2))
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_hud(screen, car, track):
    # If race is finished, show final lap and big FINISHED text
    if car.finished:
        lap_text = f"Lap {track['laps']} / {track['laps']}"
        draw_text_with_shadow(lap_text, 20, 20)
        draw_text_with_shadow("FINISHED!", SCREEN_RES[0] // 2 - 80, 20, (255, 215, 0))
        return

    # Normal lap display while racing
    lap_display = min(car.current_lap, track["laps"])
    lap_text = f"Lap {lap_display} / {track['laps']}"
    draw_text_with_shadow(lap_text, 20, 20)




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
    r = car.radius
    cx, cy = car.pos.x, car.pos.y

    for angle in range(0, 360, 45):
        offset = pygame.Vector2(r, 0).rotate(angle)
        px = int(cx + offset.x)
        py = int(cy + offset.y)

        if 0 <= px < collision_map.get_width() and 0 <= py < collision_map.get_height():
            if collision_map.get_at((px, py)) == (0, 0, 0, 255):
                normal = (car.pos - pygame.Vector2(px, py)).normalize()
                return normal

    return None


# -------------------------------
# CHECKPOINT LOGIC
# -------------------------------
def check_checkpoint(car, track):
    if car.finished:
        return

    checkpoints = track["checkpoints"]
    radius = track["checkpoint_radius"]

    target_x, target_y = checkpoints[car.next_checkpoint]
    dist = car.pos.distance_to(pygame.Vector2(target_x, target_y))

    if dist < radius:
        car.next_checkpoint += 1

        # Hit last checkpoint → next is finish line
        if car.next_checkpoint == len(checkpoints):
            car.next_checkpoint = 0
            car.ready_to_finish = True

        # Hit checkpoint 0 AND ready to finish → lap complete
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

    # Move car
    player_car.pos += player_car.velocity

    # Collision
    normal = circle_collision(player_car, collision_map)
    if normal:
        player_car.pos += normal * 2.5

        inward = player_car.velocity.dot(normal)
        if inward > 0:
            player_car.velocity -= normal * inward

        player_car.velocity += normal * 0.6
        player_car.velocity *= 0.82

        player_car.angle += normal.x * 1.2
        player_car.angle -= normal.y * 1.2

    # Checkpoint logic
    check_checkpoint(player_car, current_track)

    # Draw checkpoints (debug)
    for i, (x, y) in enumerate(current_track["checkpoints"]):
        color = (0, 255, 0) if i == player_car.next_checkpoint else (255, 255, 0)
        pygame.draw.circle(
            screen, color,
            (x - camera_offset.x, y - camera_offset.y),
            current_track["checkpoint_radius"], 2
        )

    # Draw car
    player_car.draw(screen, camera_offset)

    # Draw HUD
    draw_hud(screen, player_car, current_track)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
