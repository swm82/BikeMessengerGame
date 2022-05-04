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
        top_of_road = screen.get_height()/4
        bottom_of_road = screen.get_height()-top_of_road
        try:
            self.surface = pygame.image.load("house.png").convert_alpha()
        except:
            pass
        height = 100
        width = height * self.surface.get_width()/self.surface.get_height()
        self.surface = pygame.transform.scale(self.surface, (int(width), int(height)))

        if (is_bottom):
            self.surface = pygame.transform.rotate(self.surface, 180)


        self.surface.set_colorkey((0,0,0), RLEACCEL)

        delivery_difference = 0 if not delivery else 8
        delivery_difference = -1 * delivery_difference if is_bottom else delivery_difference

        self.rect = self.surface.get_rect(
            left=screen.get_width(), top = top_of_road-height+delivery_difference if not is_bottom else bottom_of_road+delivery_difference
        )

        self.prev_speed = 0

        self.is_delivery = delivery
        self.is_bottom = is_bottom
    
    def pause(self):
        self.speed = 0

    def resume(self):
        self.speed = 2
    

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            if self.is_delivery:
                pygame.event.post(self.HOUSE_MISS_EVENT)