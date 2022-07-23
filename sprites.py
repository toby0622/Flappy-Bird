import pygame
from settings import *


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

    def update(self, dt):
        self.position.x -= 360 * dt

        if self.rect.centerx <= 0:
            self.position.x = 0

        self.rect.x = round(self.position.x)    
