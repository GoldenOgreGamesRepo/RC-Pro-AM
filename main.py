import pygame
import sys
from car import Car
from settings import SCREEN_RES, GAME_BG, FPS, TRACKS

pygame.init()

# -------------------------------
# GLOBAL GAME STATE
# -------------------------------
game_state = "title"      # title → mode_select → arcade_track_select → arcade_car_select → race → results
race_state = "idle"       # idle → countdown → racing → results

# -------------------------------
# BASIC SETUP
# -------------------------------
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("R.C. Python Game")
clock = pygame.time.Clock()

# -------------------------------
# TRACK / CAR PLACEHOLDERS
# -------------------------------
track_list = ["track_1", "track_2", "track_3", "track_4", "track_5"]

current_track = None
track = None
collision_map = None
player_car = None

selected_option = 0
selected_track = 0
chosen_track = None

countdown_time = 3.0


# -------------------------------
# DRAW HELPERS
# -------------------------------
def draw_text_with_shadow(text, x, y, color=(255,255,255)):
    shadow = font.render(text, True, (0, 0, 0))
    screen.blit(shadow, (x + 2, y + 2))
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


# -------------------------------
# TITLE SCREEN
# -------------------------------
def draw_title_screen():
    draw_text_with_shadow("R.C. PYTHON", SCREEN_RES[0]//2 - 120, 120, (255, 215, 0))
    draw_text_with_shadow("Press ENTER to Start", SCREEN_RES[0]//2 - 140, 260)


# -------------------------------
# MODE SELECT
# -------------------------------
def draw_mode_select(selected):
    options = ["Arcade", "Career", "Time Trial"]
    for i, opt in enumerate(options):
        color = (255, 255, 0) if i == selected else (255, 255, 255)
        draw_text_with_shadow(opt, SCREEN_RES[0]//2 - 60, 200 + i*40, color)


# -------------------------------
# TRACK SELECT
# -------------------------------
def draw_track_select(selected, tracks):
    draw_text_with_shadow("Select Track", SCREEN_RES[0]//2 - 80, 120)
    for i, t in enumerate(tracks):
        color = (255, 255, 0) if i == selected else (255, 255, 255)
        draw_text_with_shadow(t, SCREEN_RES[0]//2 - 60, 200 + i*40, color)


# -------------------------------
# CAR SELECT
# -------------------------------
def draw_car_select():
    draw_text_with_shadow("Select Car", SCREEN_RES[0]//2 - 80, 120)
    draw_text_with_shadow("Car 1", SCREEN_RES[0]//2 - 40, 200, (255,255,0))


# -------------------------------
# RESULTS SCREEN
# -------------------------------
def draw_results(car, track):
    draw_text_with_shadow("RACE COMPLETE!", SCREEN_RES[0]//2 - 120, 120, (255, 215, 0))
    draw_text_with_shadow(f"Laps: {track['laps']} / {track['laps']}", SCREEN_RES[0]//2 - 80, 200)
    draw_text_with_shadow("Press ENTER to continue", SCREEN_RES[0]//2 - 140, 300, (200, 200, 200))


# -------------------------------
# COUNTDOWN
# -------------------------------
def draw_countdown(time_left):
    if time_left > 2:
        text = "3"
    elif time_left > 1:
        text = "2"
    elif time_left > 0:
        text = "1"
    else:
        text = "GO!"
    draw_text_with_shadow(text, SCREEN_RES[0]//2 - 20, SCREEN_RES[1]//2 - 40, (255, 255, 0))


# -------------------------------
# HUD
# -------------------------------
def draw_hud(car, track):
    if car.finished:
        draw_text_with_shadow(f"Lap {track['laps']} / {track['laps']}", 20, 20)
        draw_text_with_shadow("FINISHED!", SCREEN_RES[0]//2 - 80, 20, (255, 215, 0))
        return

    lap_display = min(car.current_lap, track["laps"])
    draw_text_with_shadow(f"Lap {lap_display} / {track['laps']}", 20, 20)


# -------------------------------
# CAMERA
# -------------------------------
def get_camera_offset(player_pos):
    return pygame.Vector2(
        player_pos.x - SCREEN_RES[0] // 2,
        player_pos.y - SCREEN_RES[1] // 2
    )


# -------------------------------
# COLLISION
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
                return (car.pos - pygame.Vector2(px, py)).normalize()

    return None


# -------------------------------
# LOAD TRACK
# -------------------------------
def load_track(track_name):
    global current_track, track, collision_map, player_car

    current_track = TRACKS[track_name]
    track = pygame.image.load(current_track["image"]).convert()
    collision_map = pygame.image.load(current_track["collision"]).convert()

    start_x, start_y = current_track["start_pos"]
    player_car = Car(start_x, start_y, "car_1.png")
    player_car.angle = current_track["start_angle"]


# -------------------------------
# CHECKPOINT LOGIC
# -------------------------------
def check_checkpoint(car, track):
    global race_state, game_state

    if car.finished:
        return

    checkpoints = track["checkpoints"]
    radius = track["checkpoint_radius"]

    target_x, target_y = checkpoints[car.next_checkpoint]
    dist = car.pos.distance_to(pygame.Vector2(target_x, target_y))

    if dist < radius:
        car.next_checkpoint += 1

        if car.next_checkpoint == len(checkpoints):
            car.next_checkpoint = 0
            car.ready_to_finish = True

        elif car.next_checkpoint == 1 and car.ready_to_finish:
            car.current_lap += 1
            car.ready_to_finish = False

            if car.current_lap > track["laps"]:
                car.finished = True
                race_state = "results"
                game_state = "results"


# -------------------------------
# GAME LOOP
# -------------------------------
running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # TITLE
        if game_state == "title":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "mode_select"
                selected_option = 0

        # MODE SELECT
        elif game_state == "mode_select":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 3
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 3
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        game_state = "arcade_track_select"
                        selected_track = 0
                    elif selected_option == 1:
                        print("Career mode coming soon")
                    elif selected_option == 2:
                        print("Time Trial coming soon")

        # TRACK SELECT
        elif game_state == "arcade_track_select":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_track = (selected_track - 1) % len(track_list)
                if event.key == pygame.K_DOWN:
                    selected_track = (selected_track + 1) % len(track_list)
                if event.key == pygame.K_RETURN:
                    chosen_track = track_list[selected_track]
                    game_state = "arcade_car_select"
                if event.key == pygame.K_ESCAPE:
                    game_state = "mode_select"

        # CAR SELECT
        elif game_state == "arcade_car_select":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    load_track(chosen_track)
                    game_state = "race"
                    race_state = "countdown"
                    countdown_time = 3.0
                if event.key == pygame.K_ESCAPE:
                    game_state = "arcade_track_select"

        # RESULTS
        elif game_state == "results":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "arcade_track_select"


    # -------------------------------
    # DRAW SCREENS
    # -------------------------------
    screen.fill(GAME_BG)

    if game_state == "title":
        draw_title_screen()

    elif game_state == "mode_select":
        draw_mode_select(selected_option)

    elif game_state == "arcade_track_select":
        draw_track_select(selected_track, track_list)

    elif game_state == "arcade_car_select":
        draw_car_select()

    elif game_state == "results":
        draw_results(player_car, current_track)

    elif game_state == "race":

        camera_offset = get_camera_offset(player_car.pos)
        screen.blit(track, (-camera_offset.x, -camera_offset.y))

        dt = clock.get_time() / 1000.0

        if race_state == "countdown":
            countdown_time -= dt
            if countdown_time <= 0:
                race_state = "racing"

        if race_state == "racing":
            player_car.update()
            player_car.pos += player_car.velocity

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

        check_checkpoint(player_car, current_track)

        for i, (x, y) in enumerate(current_track["checkpoints"]):
            color = (0, 255, 0) if i == player_car.next_checkpoint else (255, 255, 0)
            pygame.draw.circle(
                screen, color,
                (x - camera_offset.x, y - camera_offset.y),
                current_track["checkpoint_radius"], 2
            )

        player_car.draw(screen, camera_offset)

        if race_state == "countdown":
            draw_countdown(countdown_time)

        draw_hud(player_car, current_track)

        if race_state == "results":
            draw_results(player_car, current_track)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
