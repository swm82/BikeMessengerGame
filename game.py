import pygame
from player import Player
from car import Car
from road import Road

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
PLAYER_MOVE_SENSITIVITY = 5 # num pixels moved per key press
NUM_LANES = 4

speed = [2, 0]
grass_rgb = 8, 69, 24

screen = pygame.display.set_mode(SCREEN_SIZE) # Create display window (special Surface)

ADDCAR = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCAR, 500)

road = Road(screen, NUM_LANES)
player = Player(screen)

all_sprites = pygame.sprite.Group()
cars = pygame.sprite.Group()
all_sprites.add(player)

print(road.get_car_y_coords())

# The game loop:
running = True
while running:
    # Check for input
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        elif event.type == ADDCAR:
            car = Car(screen, road.get_dimensions(), road.get_car_y_coords())
            cars.add(car)
            all_sprites.add(car)

    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # update car locations
    cars.update()

    # Clear screen
    screen.fill(grass_rgb)

    road.draw_road()

    for sprite in all_sprites:
        screen.blit(sprite.surface, sprite.rect)

    # Check for collision
    if pygame.sprite.spritecollideany(player, cars):
        player.kill()
        running = False

    # Swap double buffer
    pygame.display.flip()
    # TODO: Look into using dirty rect animation (using display.update(list of updated rectangles))
        # http://www.pygame.org/docs/tut/newbieguide.html
