import pygame
from settings import *
from random import choice, randint


class Background(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        background_image = pygame.image.load('graphics/environment/background.png').convert()
        # Background Image Attributes
        full_height = background_image.get_height() * scale_factor
        full_width = background_image.get_width() * scale_factor
        full_size_image = pygame.transform.scale(background_image, (full_width, full_height))
        # Paste Background Image Twice
        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_size_image, (0, 0))
        self.image.blit(full_size_image, (full_width, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.position = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.position.x -= 300 * dt

        if self.rect.centerx <= 0:
            self.position.x = 0

        self.rect.x = round(self.position.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # Image
        ground_surface = pygame.image.load('graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surface,
                                            pygame.math.Vector2(ground_surface.get_size()) * scale_factor)
        # Position
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.position = pygame.math.Vector2(self.rect.topleft)
        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.position.x -= 360 * dt

        if self.rect.centerx <= 0:
            self.position.x = 0

        self.rect.x = round(self.position.x)


class Plane(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # Image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        # Rect
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.position = pygame.math.Vector2(self.rect.topleft)
        # Movement
        self.gravity = 600
        self.direction = 0
        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def import_frames(self, scale_factor):
        self.frames = []

        for i in range(3):
            surface = pygame.image.load(f'graphics/plane/red{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surface, pygame.math.Vector2(surface.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.position.y += self.direction * dt
        self.rect.y = round(self.position.y)

    def jump(self):
        self.direction = (-400)

    def animate(self, dt):
        self.frame_index += 20 * dt

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotated_plane
        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        orientation = choice(('up', 'down'))
        surface = pygame.image.load(f'graphics/obstacles/{choice((0, 1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surface, pygame.math.Vector2(surface.get_size()) * scale_factor)

        x = WINDOW_WIDTH + randint(40, 100)

        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            y = randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop=(x, y))

        self.position = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.position.x -= 400 * dt
        self.rect.x = round(self.position.x)

        if self.rect.right <= -100:
            self.kill()
