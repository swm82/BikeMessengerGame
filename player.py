import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, road, sensitivity = 5):
        super(Player, self).__init__()
        # self.surface = pygame.Surface((40,10))
        # self.surface.fill((255,255,255))
        self.screen = screen
        self.sensitivity = sensitivity
        self.road = road

        self.surface = pygame.image.load("biker.png").convert_alpha()
        height = road.get_lane_width()
        width = height * self.surface.get_width()/self.surface.get_height()
        self.surface = pygame.transform.scale(self.surface, (int(width), int(height)))
        self.rect = self.surface.get_rect(left=0, top = self.screen.get_height()/4)
        self.is_safe = False

    def update(self, pressed_keys):
        # if self.is_safe:
        #     if self.is_safe.is_bottom:
        #         key = K_UP
        #         move = -50
        #     else:
        #         key = K_DOWN
        #         move = 50
        #     if pressed_keys[key]:
        #         self.rect.move_ip(0, move)
        #         self.is_safe = None
        # else:
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.sensitivity)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.sensitivity)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.sensitivity, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.sensitivity, 0)

        # Clamp the player into the screen
        self.rect.clamp_ip(self.road.pavement_rect)
        # self.rect.clamp_ip(self.screen.get_rect())
    
    def respawn(self):
        self.rect = self.surface.get_rect(left = 0, top = self.screen.get_height()/4)

    def move_to_safety(self, house):
        print("HERE")
        if house.is_bottom:
            self.rect.y += 100
            # self.rect.move_ip(0, 100)
        else:
            self.rect.y -= 100
            # self.rect.move_ip(0, -100)

        self.is_safe = house
