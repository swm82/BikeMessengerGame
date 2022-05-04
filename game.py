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
    K_RETURN
)

pygame.init()

# Constants, parameters, state, etc.
# Parameters
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
PLAYER_MOVE_SENSITIVITY = 5 # num pixels moved per key press

# Events
ADDCAR = pygame.USEREVENT # Triggers a new car
HOUSE_MISS = pygame.USEREVENT + 1 # Triggered when a delivery house goes off screen.. point deduction
INVINCIBLE = pygame.USEREVENT + 2 # Give the player time to get free before losing lives

# Styling
PADDING_R = PADDING_L = PADDING_T = PADDING_B = 20
COLOR_GRASS = 8, 69, 24

class Game:
    NUM_LANES = 3 # Number of lanes per side of the road
    MAX_SPEED = 7 # Max car speed.  Increases as level advances
    DELIVERY_FREQUENCY = 5 # Every n'th house is a delivery
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

        self.game_over = False

        # Set event timers
        self.car_timing = 1000
        pygame.time.set_timer(ADDCAR, self.car_timing)

    def new_round(self):
        self.houses_since_delivery = 1
        self.last_house_top = None
        self.last_house_bottom = None
        self.init_objects()

    
    def draw_text(self):
        lives_txt = self.fonts['stats'].render(f'Lives: {self.num_lives}', True, (255,255,255))
        score_txt = self.fonts['stats'].render(f'Score: {self.points}', True, (255,255,255))
        level_txt = self.fonts['stats'].render(f'Level: {self.level}', True, (255,255,255))

        self.screen.blit(lives_txt, (SCREEN_WIDTH - lives_txt.get_width()-PADDING_R,0))
        self.screen.blit(score_txt, (PADDING_L, 0))
        self.screen.blit(level_txt, (SCREEN_WIDTH//2 - level_txt.get_width()//2,0))

        if self.game_over:
            game_over_text = self.fonts['game_over'].render('GAME OVER', True, (255,255,255))
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2-game_over_text.get_height()))
            instructs = self.fonts['stats'].render('Press ENTER to play again', True, (255,255,255))
            self.screen.blit(instructs, (SCREEN_WIDTH//2 - instructs.get_width()//2, SCREEN_HEIGHT//2 + game_over_text.get_height()//2))


    def init_objects(self):
        # Objects
        self.objects['road'] = Road(self.screen, Game.NUM_LANES)

        # Sprite Groups
        self.objects['all_sprites']= pygame.sprite.Group()
        self.objects['house_sprites'] = pygame.sprite.Group()
        self.objects['car_sprites']= pygame.sprite.Group()

        # Sprites
        self.objects['player'] = Player(self.screen, self.objects['road'])
        self.objects['all_sprites'].add(self.objects['player'])
        
        Car.cars_arr = [None] * Game.NUM_LANES*2

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
        self.fonts['game_over'] = pygame.font.SysFont("comicsansms", 120)

        # Delivery marker
        self.env_surface = pygame.image.load("env.png").convert_alpha()
        height = 50
        width = height * self.env_surface.get_width()/self.env_surface.get_height()
        self.env_surface = pygame.transform.scale(self.env_surface, (int(width), int(height)))

    def stop_background(self, enable):
        if enable:
            self.objects['road'].pause()
        else:
            self.objects['road'].resume()

        for house in self.objects['house_sprites'].sprites():
            if enable:
                house.pause()
            else:
                house.resume()


    def handle_collision(self):
        if self.num_lives == 0:
            # TODO: handle_game_over()
            # self.handle_game_over()
            self.game_over = True
            self.stop_background(True)
        else:
            self.num_lives -= 1
            self.objects['player'] = Player(self.screen, self.objects['road'])
            self.objects['player'].is_safe = True
            self.objects['all_sprites'].add(self.objects['player'])
            pygame.time.set_timer(INVINCIBLE, 2000)
    
    def handle_delivery(self, house):
        self.objects['player'].move_to_safety(house)
        if self.points >= self.level * 3:
            self.level += 1
            Game.NUM_LANES += 1
            self.car_timing = max(self.car_timing-200, 0)

            pygame.time.set_timer(ADDCAR, self.car_timing)
            Game.MAX_SPEED += min(Game.MAX_SPEED, 1)
            Game.DELIVERY_FREQUENCY = max(Game.DELIVERY_FREQUENCY -1, 0)
            self.new_round()

    def add_house(self):
        if self.last_house_top and self.screen.get_rect().contains(self.last_house_top):
            delivery = self.houses_since_delivery >= Game.DELIVERY_FREQUENCY # Time for another delivery

            # Randomly determine if the delivery is at top or bottom
            rand_num = random.randint(0,1)
            top = rand_num % 2 == 0

            house_top = House(self.screen, HOUSE_MISS, delivery and top)
            house_bottom = House(self.screen, HOUSE_MISS, delivery and not top, is_bottom=True)
            self.houses_since_delivery += 1

            if delivery:
                # Reset number of houses
                self.houses_since_delivery = 0
                # Create sprite for mailbox

            self.objects['house_sprites'].add(house_top)
            self.objects['house_sprites'].add(house_bottom)
            self.objects['all_sprites'].add(house_top)
            self.objects['all_sprites'].add(house_bottom)
            self.last_house_top = house_top
            self.last_house_bottom = house_bottom

    def run_game_loop(self):

        collide_did_occur_car = False
        collide_did_occur_house = False

        running = True
        while running:
            # Add another house once the previous one is fully  on the screen
            self.add_house()

            # Process events
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False
                elif event.type == ADDCAR:
                    car = Car(self.screen, self.objects['road'], Game.MAX_SPEED)
                    self.objects['car_sprites'].add(car)
                    self.objects['all_sprites'].add(car)
                elif event.type == HOUSE_MISS:
                    self.points -= 1
                elif event.type == INVINCIBLE:
                    self.objects['player'].is_safe = False
                elif self.game_over and event.type == KEYDOWN and event.key == K_RETURN:
                    Game.NUM_LANES = 3 # Number of lanes per side of the road
                    Game.MAX_SPEED = 7 # Max car speed.  Increases as level advances
                    Game.DELIVERY_FREQUENCY = 5 # Every n'th house is a delivery
                    self.new_round()
                    self.game_over = False
                    self.stop_background(False)
                    self.num_lives = 3
                    self.points = 0
                

            pressed_keys = pygame.key.get_pressed()


            # update car locations
            self.objects['car_sprites'].update()

            self.objects['house_sprites'].update()

            # Update the player sprite based on user keypresses
            self.objects['player'].update(pressed_keys)

            # Clear screen
            self.screen.fill(COLOR_GRASS)

            self.objects['road'].draw_road()

            for sprite in self.objects['all_sprites']:
                self.screen.blit(sprite.surface, sprite.rect)
                if isinstance(sprite, House) and sprite.is_delivery:
                    self.screen.blit(self.env_surface, sprite.rect)

            if pygame.sprite.spritecollideany(self.objects['player'], self.objects['car_sprites']) and not self.objects['player'].is_safe:
                collide_did_occur_car = True
                self.objects['player'].kill()
            elif collide_did_occur_car:
                self.handle_collision()
                collide_did_occur_car = False

            if res := pygame.sprite.spritecollideany(self.objects['player'], self.objects['house_sprites']):
                if res.is_delivery:
                    res.is_delivery = False
                    if not collide_did_occur_house: # Prevents incrementing points while the sprites are collided
                        self.points += 1
                        collide_did_occur_house = True
                    self.stop_background(True)
                    self.handle_delivery(res)
            elif collide_did_occur_house:
                self.stop_background(False)
                collide_did_occur_house = False


            self.draw_text()
            
            # Swap double buffer
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run_game_loop()
