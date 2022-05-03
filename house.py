import pygame
import random

from pygame.locals import (
    RLEACCEL
)

class House(pygame.sprite.Sprite):
    def __init__(self, screen, HOUSE_MISS_EVENT, delivery=False, is_bottom=False):
        super(House, self).__init__()
        self.speed = 2
        self.HOUSE_MISS_EVENT = pygame.event.Event(HOUSE_MISS_EVENT)
        print()
        top_of_road = screen.get_height()/4
        bottom_of_road = screen.get_height()-top_of_road
        self.surface = pygame.image.load("house.png").convert_alpha()
        height = 100
        width = height * self.surface.get_width()/self.surface.get_height()
        self.surface = pygame.transform.scale(self.surface, (int(width), int(height)))

        if (is_bottom):
            self.surface = pygame.transform.rotate(self.surface, 180)


        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect(
            left=screen.get_width(), top = top_of_road-height if not is_bottom else bottom_of_road
        )

        self.is_delivery = delivery
    

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            if self.is_delivery:
                pygame.event.post(self.HOUSE_MISS_EVENT)
                print("YEP")