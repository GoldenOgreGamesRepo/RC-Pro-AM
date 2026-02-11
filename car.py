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

    # Input
    def handle_input(self):
           # Handle key presses for car control
        keys = pygame.key.get_pressed()
        # Only turn if the car is actually moving
        if self.velocity.length() > 0.1:
            if keys[pygame.K_LEFT]:
                self.angle += self.turn_speed
            if keys[pygame.K_RIGHT]:
                self.angle -= self.turn_speed

        if self.velocity.length() > 0.2:
            if keys[pygame.K_LEFT]:
                self.angle += self.turn_speed
            if keys[pygame.K_RIGHT]:
                self.angle -= self.turn_speed

        # Forward movement
        if keys[pygame.K_UP] :
            direction = pygame.Vector2(1, 0).rotate(-self.angle) 
            self.velocity += direction * self.acceleration
        if keys[pygame.K_DOWN]: 
            direction = pygame.Vector2(1, 0).rotate(-self.angle) 
            self.velocity -= direction * (self.acceleration * 0.5)

    # Physics
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

    def draw(self, screen):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        screen.blit(self.image, self.rect)
