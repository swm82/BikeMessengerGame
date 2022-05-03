import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, sensitivity = 5):
        super(Player, self).__init__()
        self.surface = pygame.Surface((40,10))
        self.surface.fill((255,255,255))
        self.rect = self.surface.get_rect()
        self.screen = screen
        self.sensitivity = sensitivity

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.sensitivity)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.sensitivity)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.sensitivity, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.sensitivity, 0)

        # Clamp the player into the screen
        self.rect.clamp_ip(self.screen.get_rect())
    
    def respawn(self):
        self.rect.update(0,0, 40,10)