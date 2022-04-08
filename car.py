import pygame, random
from pygame.locals import (
    RLEACCEL
)

class Car(pygame.sprite.Sprite):
    def __init__(self, screen, road_dimensions, lane_y_coords):
        super(Car, self).__init__()
        self.surface = pygame.image.load("carstop.png").convert() # Returns surface with ball data 
        self.surface.set_colorkey((0,0,0), RLEACCEL)

        self.rect = self.surface.get_rect(
            center=(
                # random.randint(road_dimensions[1] + 20, road_dimensions[0] + 100),
                screen.get_width(),
                # random.randint(0, road_dimensions[1])+screen.get_height()/4, # offset the y coord
                lane_y_coords[random.randint(0, len(lane_y_coords)-1)]
            )
        )
        self.min_speed = 5
        self.max_speed = 7
        self.speed = random.randint(self.min_speed, self.max_speed)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()