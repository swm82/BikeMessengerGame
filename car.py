import pygame, random
from pygame.locals import (
    RLEACCEL
)

class Car(pygame.sprite.Sprite):
    def __init__(self, screen, road, max_speed):
        super(Car, self).__init__()

        # Set up car surface.  Scale car to fit lane
        self.surface = pygame.image.load("carstop.png").convert() # Returns surface with ball data 
        lane_width = road.get_lane_width()
        height = lane_width
        width = height * self.surface.get_width()/self.surface.get_height()
        self.surface = pygame.transform.scale(self.surface, (int(width), int(height)))
        self.surface.set_colorkey((0,0,0), RLEACCEL)

        car_lanes = road.get_car_y_coords()
        self.rect = self.surface.get_rect(
            center=(
                # random.randint(road_dimensions[1] + 20, road_dimensions[0] + 100),
                screen.get_width() + width/2,
                # random.randint(0, road_dimensions[1])+screen.get_height()/4, # offset the y coord
                car_lanes[random.randint(0, len(car_lanes)-1)]
            )
        )

        self.min_speed = 5
        self.max_speed = max_speed
        self.speed = random.randint(self.min_speed, self.max_speed)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()