import pygame

class Car:
    def __init__(self, x, y, image_path):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0
        self.velocity = pygame.Vector2(2, 0)

        # Physics parameters
        self.acceleration = 0.18
        self.friction = 0.12  
        self.turn_speed = 1.2 
        self.max_speed = 5

        # Load sprite
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.pos)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Only turn if the car is actually moving
        if self.velocity.length() > 0.1:
            if keys[pygame.K_LEFT]:
                self.angle += self.turn_speed
            if keys[pygame.K_RIGHT]:
                self.angle -= self.turn_speed

        # Forward movement
        if keys[pygame.K_UP]:
            direction = pygame.Vector2(1, 0).rotate(-self.angle)
            self.velocity += direction * self.acceleration

        # Reverse / braking
        if keys[pygame.K_DOWN]:
            direction = pygame.Vector2(1, 0).rotate(-self.angle)
            self.velocity -= direction * (self.acceleration * 0.5)

    def apply_physics(self):
        # Friction
        if self.velocity.length() > self.friction:
            self.velocity -= self.velocity.normalize() * self.friction
        else:
            self.velocity = pygame.Vector2(0, 0)

        # Clamp speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # Move
        self.pos += self.velocity

    def update(self):
        self.handle_input()
        self.apply_physics()

    def draw(self, screen, camera_offset):
        # Rotate the sprite
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)

        # Convert world position → screen position
        screen_pos = self.pos - camera_offset

        # Center the rotated image on the screen position
        rect = rotated_image.get_rect(center=screen_pos)

        # Draw it
        screen.blit(rotated_image, rect)

