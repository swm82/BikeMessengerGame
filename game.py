import pygame
from player import Player
from car import Car
from road import Road
from house import House
import random

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Constants, parameters, state, etc.
# Parameters
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
PLAYER_MOVE_SENSITIVITY = 5 # num pixels moved per key press
NUM_LANES = 6 # Number of lanes per side of the road
MAX_SPEED = 7 # Max car speed.  Increases as level advances
DELIVERY_FREQUENCY = 10 # Every n'th house is a delivery

# Events
ADDCAR = pygame.USEREVENT # Triggers a new car
HOUSE_MISS = pygame.USEREVENT + 1 # Triggered when a delivery house goes off screen.. point deduction
DELIVERY = pygame.USEREVENT + 2

# Styling
PADDING_R = PADDING_L = PADDING_T = PADDING_B = 20
COLOR_GRASS = 8, 69, 24

class Game:
    def __init__(self):
        # Creates stats
        self.num_lives, self.points, self.level = 3, 0, 1
        self.screen = pygame.display.set_mode(SCREEN_SIZE) # Create display window (special Surface)

        """
        Displayable objects dict
        'player' - Player sprite object
        'road' - Road object - which contains all the primitives used to draw the background, moving road, houses
        'all_sprites' - Sprite group containing all living sprites
        'house_sprites' - Living house sprites
        'car_sprites' - Living car sprites
        """
        self.objects = {} # Displayable objects dict.
        """
        dict of "font" objects, used for displaying font
        'stats' - used for printing lives, score, level stats
        """
        self.fonts = {} # Font objects used to print to screen

        # House flags and data
        self.houses_since_delivery = 1
        self.last_house_top = None # Ref to the last house on the screen (to the right) - above road
        self.last_house_bottom = None # Ref to the last house on the screen (to the right) - below road

        self.init_objects()

        # Set event timers
        pygame.time.set_timer(ADDCAR, 500)
        pygame.time.set_timer(DELIVERY, 10000)

    
    def draw_text(self):
        lives_txt = self.fonts['stats'].render(f'Lives: {self.num_lives}', True, (255,255,255))
        score_txt = self.fonts['stats'].render(f'Score: {self.points}', True, (255,255,255))
        level_txt = self.fonts['stats'].render(f'Level: {self.level}', True, (255,255,255))

        self.screen.blit(lives_txt, (SCREEN_WIDTH - lives_txt.get_width()-PADDING_R,0))
        self.screen.blit(score_txt, (PADDING_L, 0))
        self.screen.blit(level_txt, (SCREEN_WIDTH//2 - level_txt.get_width()//2,0))

    def init_objects(self):
        # Objects
        self.objects['road'] = Road(self.screen, NUM_LANES)

        # Sprite Groups
        self.objects['all_sprites']= pygame.sprite.Group()
        self.objects['house_sprites'] = pygame.sprite.Group()
        self.objects['car_sprites']= pygame.sprite.Group()

        # Sprites
        self.objects['player'] = Player(self.screen)
        self.objects['all_sprites'].add(self.objects['player'])
        
        Car.cars_arr = [None] * NUM_LANES*2

        # First 2 houses (one on top, one on bottom of road)
        house = House(self.screen, HOUSE_MISS)
        self.objects['house_sprites'].add(house)
        self.objects['all_sprites'].add(house)
        self.last_house_top = house
        house = House(self.screen, HOUSE_MISS, is_bottom=True)
        self.objects['house_sprites'].add(house)
        self.objects['all_sprites'].add(house)
        self.last_house_bottom = house
        self.houses_since_delivery = 1

        self.fonts['stats'] = pygame.font.SysFont("comicsansms", 24)

    def handle_collision(self):
        if self.num_lives == 0:
            # TODO: handle_game_over()
            print("GAMEOVER")
        else:
            self.objects['player'].respawn()
    
    def run_game_loop(self):

        collide_did_occur = False

        running = True
        while running:
            # Add another house once the previous one is fully  on the screen
            if self.last_house_top and self.screen.get_rect().contains(self.last_house_top):
                delivery = self.houses_since_delivery >= DELIVERY_FREQUENCY # Time for another delivery

                # Randomly determine if the delivery is at top or bottom
                rand_num = random.randint(0,1)
                top = rand_num % 2 == 0

                house_top = House(self.screen, HOUSE_MISS, delivery and top)
                house_bottom = House(self.screen, HOUSE_MISS, delivery and not top, is_bottom=True)
                self.houses_since_delivery += 1

                if delivery:
                    # Reset number of houses
                    self.houses_since_delivery = 0

                self.objects['house_sprites'].add(house_top)
                self.objects['house_sprites'].add(house_bottom)
                self.objects['all_sprites'].add(house_top)
                self.objects['all_sprites'].add(house_bottom)
                self.last_house_top = house_top
                self.last_house_bottom = house_bottom

            # Process events
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False
                elif event.type == ADDCAR:
                    car = Car(self.screen, self.objects['road'], MAX_SPEED)
                    self.objects['car_sprites'].add(car)
                    self.objects['all_sprites'].add(car)
                elif event.type == HOUSE_MISS:
                    self.points -= 1

            pressed_keys = pygame.key.get_pressed()

            # Update the player sprite based on user keypresses
            self.objects['player'].update(pressed_keys)

            # update car locations
            self.objects['car_sprites'].update()

            self.objects['house_sprites'].update()

            # Clear screen
            self.screen.fill(COLOR_GRASS)

            self.objects['road'].draw_road()

            for sprite in self.objects['all_sprites']:
                self.screen.blit(sprite.surface, sprite.rect)

            # Check for collision
            if pygame.sprite.spritecollideany(self.objects['player'], self.objects['car_sprites']):
                # if num_lives < 0:
                collide_did_occur = True
                #     handle_game_over()
                # player.kill()
                # running = False
                self.objects['player'].respawn()
            else:
                if collide_did_occur:
                    self.num_lives -= 1
                    collide_did_occur = False

            self.draw_text()
            
            # Swap double buffer
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run_game_loop()



# pygame.init()

# # Parameters
# SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
# PLAYER_MOVE_SENSITIVITY = 5 # num pixels moved per key press
# NUM_LANES = 6 # Number of lanes per side of the road
# MAX_SPEED = 7 # Max car speed.  Increases as level advances
# DELIVERY_FREQUENCY = 10 # Every n'th house is a delivery

# # Events
# ADDCAR = pygame.USEREVENT # Triggers a new car
# HOUSE_MISS = pygame.USEREVENT + 1 # Triggered when a delivery house goes off screen.. point deduction
# DELIVERY = pygame.USEREVENT + 2

# # Styling
# PADDING_R = PADDING_L = PADDING_T = PADDING_B = 20
# COLOR_GRASS = 8, 69, 24

# Stats
# num_lives = 3
# points = 0
# level = 1

# speed = [2, 0]

# grass_rgb = 8, 69, 24

# screen = pygame.display.set_mode(SCREEN_SIZE) # Create display window (special Surface)

# pygame.time.set_timer(ADDCAR, 500)
# pygame.time.set_timer(DELIVERY, 10000)

# road = Road(screen, NUM_LANES)
# player = Player(screen)

# all_sprites = pygame.sprite.Group()
# cars = pygame.sprite.Group()
# Car.cars_arr = [None] * NUM_LANES*2
# print(Car.cars_arr)
# houses = pygame.sprite.Group()
# all_sprites.add(player)


# # Font

# stats_font = pygame.font.SysFont("comicsansms", 24)

# def draw_text():
#     lives_txt = stats_font.render(f'Lives: {num_lives}', True, (255,255,255))
#     score_txt = stats_font.render(f'Score: {points}', True, (255,255,255))
#     level_txt = stats_font.render(f'Level: {level}', True, (255,255,255))

#     screen.blit(lives_txt, (SCREEN_WIDTH - lives_txt.get_width()-PADDING_R,0))
#     screen.blit(score_txt, (PADDING_L, 0))
#     screen.blit(lives_txt, (SCREEN_WIDTH//2 - level_txt.get_width()//2,0))

# collide_did_occur = False


# def handle_collision():
#     if num_lives == 0:
#         # TODO: handle_game_over()
#         print("GAMEOVER")
#     else:
#         player.respawn()


# house = House(screen, HOUSE_MISS)
# houses.add(house)
# all_sprites.add(house)
# last_house_top = house
# house = House(screen, HOUSE_MISS, is_bottom=True)
# houses.add(house)
# all_sprites.add(house)
# last_house_bottom = house
# houses_since_delivery = 1

# delivery = False

# # The game loop:
# running = True
# while running:
#     # Add another house once the previous one is fully  on the screen
#     if last_house_top and screen.get_rect().contains(last_house_top):
#         delivery = houses_since_delivery >= DELIVERY_FREQUENCY # Time for another delivery
#         print(delivery)
#         rand_num = random.randint(0,1)

#         # Randomly determine if the delivery is at top or bottom
#         top = rand_num % 2 == 0

#         house_top = House(screen, HOUSE_MISS, delivery and top)
#         house_bottom = House(screen, HOUSE_MISS, delivery and not top, is_bottom=True)
#         houses_since_delivery += 1

#         if delivery:
#             # Reset number of houses
#             houses_since_delivery = 0
#         houses.add(house_top)
#         houses.add(house_bottom)
#         all_sprites.add(house_top)
#         all_sprites.add(house_bottom)
#         last_house_top = house_top
#         last_house_bottom = house_bottom

#     # Check for input
#     for event in pygame.event.get():
#         if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
#             running = False
#         elif event.type == ADDCAR:
#             car = Car(screen, road, MAX_SPEED)
#             cars.add(car)
#             all_sprites.add(car)
#         elif event.type == HOUSE_MISS:
#             points -= 1

#     pressed_keys = pygame.key.get_pressed()

#     # Update the player sprite based on user keypresses
#     player.update(pressed_keys)

#     # update car locations
#     cars.update()

#     houses.update()

#     # Clear screen
#     screen.fill(grass_rgb)

#     road.draw_road()

#     for sprite in all_sprites:
#         screen.blit(sprite.surface, sprite.rect)

#     # Check for collision
#     if pygame.sprite.spritecollideany(player, cars):
#         # if num_lives < 0:
#         collide_did_occur = True
#         #     handle_game_over()
#         # player.kill()
#         # running = False
#         player.respawn()
#     else:
#         if collide_did_occur:
#             num_lives -= 1
#             collide_did_occur = False

#     draw_text()
    

#     # Swap double buffer
#     pygame.display.flip()
#     # TODO: Look into using dirty rect animation (using display.update(list of updated rectangles))
#         # http://www.pygame.org/docs/tut/newbieguide.html
