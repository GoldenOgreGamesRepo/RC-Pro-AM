import pygame
import math

class Car:
    def __init__(self, x, y, image_path):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0
        self.velocity = pygame.Vector2(0, 0)

        # Load sprite
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.pos)

        # Circle collider radius (tune this!)
        self.radius = self.image.get_width() * 0.40  # 40% of width works great

        # Physics parameters
        self.acceleration = 0.18
        self.friction = 0.12
        self.turn_speed = 1.2
        self.max_speed = 5

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Only turn if the car is actually moving
        if self.velocity.length() > 0.1:
            if keys[pygame.K_LEFT]:
                self.angle += self.turn_speed
            if keys[pygame.K_RIGHT]:
                self.angle -= self.turn_speed

        # Forward
        if keys[pygame.K_UP]:
            direction = pygame.Vector2(1, 0).rotate(-self.angle)
            self.velocity += direction * self.acceleration

        # Reverse
        if keys[pygame.K_DOWN]:
            direction = pygame.Vector2(1, 0).rotate(-self.angle)
            self.velocity -= direction * self.acceleration

    def apply_physics(self):
        # Friction
        if self.velocity.length() > self.friction:
            self.velocity -= self.velocity.normalize() * self.friction
        else:
            self.velocity = pygame.Vector2(0, 0)

        # Clamp speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.handle_input()
        self.apply_physics()

    def draw(self, screen, camera_offset):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        screen_pos = self.pos - camera_offset
        rect = rotated_image.get_rect(center=screen_pos)
        screen.blit(rotated_image, rect)
