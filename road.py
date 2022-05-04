import pygame

class Road(pygame.sprite.Sprite):
    # Class variables
    pavement_color = (80,80,80)
    centerline_color = (252,186,3)
    def __init__(self, screen, num_lanes=2):
        super(Road, self).__init__()
        self.screen = screen

        self.num_lanes = num_lanes

        # Get these to save overhead of function calls in later calculations
        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()

        # Make the road 1/2 of the size of the screen
        self.road_size = self.screen_width, self.screen_height / 2
        # road_objects = []
        
        # Pavement background
        self.pavement = pygame.Surface(self.road_size)
        self.pavement_rect = self.pavement.get_rect(left=0, top=screen.get_height()/4)
        self.pavement.fill(Road.pavement_color)

        self.line_thickness = self.road_size[1]/80

        # Calculate coordinates of car lanes
        lane_width = (self.screen_height/2 - (3*self.line_thickness)) / (2*num_lanes)
        self.y_coords = [(self.screen_height/4) + (i*lane_width) for i in range(1, num_lanes+1)]

        bottom_half_top = self.screen_height / 2 + (1.5*self.line_thickness)
        for i in range(1,num_lanes+1):
            self.y_coords.append(bottom_half_top + (i *lane_width))

        # Yellow centerlines
        self.centerline = pygame.Surface((self.screen_width, self.line_thickness))
        self.centerline.fill(Road.centerline_color)

        # Lane line
        self.lane_line_surface = pygame.Surface((50, self.line_thickness))
        self.lane_line_surface.fill((255, 255, 255))

        self.speed = 0
        self.prev_speed = 2
        self.paused = False


    def draw_road(self):
        center_of_screen = self.screen_height / 2 
        # Top of road is 1/4 of way from top of screen
        top_of_road = center_of_screen/2

        self.screen.blit(self.pavement, (0, top_of_road))

        self.screen.blit(self.centerline, (0, center_of_screen - self.line_thickness*1.5))
        self.screen.blit(self.centerline, (0, center_of_screen + self.line_thickness/2))

        
        width_of_half_road = self.road_size[1]/2
        num_lane_lines = 10
        lane_spacing = self.lane_line_surface.get_width()

        
        for side_of_road in range(2):
            for lane in range(1,self.num_lanes):
                # draw lanes across screen
                y_offset = top_of_road + ((width_of_half_road/self.num_lanes)*lane) + side_of_road*(self.road_size[1]/2) - self.line_thickness
                for line in range(num_lane_lines):
                    # offset from x = 0
                    x_offset = (self.lane_line_surface.get_width()*line + line*lane_spacing - self.speed) % (self.road_size[0])
                    self.screen.blit(self.lane_line_surface, (x_offset, y_offset))
        self.speed = (self.speed + (0 if self.paused else 2)) % self.road_size[0]

    def get_dimensions(self):
        return self.road_size

    def get_car_y_coords(self):
        return self.y_coords


        # # TODO: Handle spacing within the lane (10*line_thickness)
        # return [top_of_road + (i*(self.road_size[1]/(self.num_lanes*2))) - 10*self.line_thickness for i in range(1,2*self.num_lanes+1)]

    def get_lane_width(self):
        # == (half of road, minus half of center line) / number of lane lines
        return ((self.road_size[1] / 2) - (2*self.line_thickness))/self.num_lanes-1


    def pause(self):
        self.paused = True
        # self.prev_speed = self.speed
        # self.speed = 0

    def resume(self):
        self.paused = False
        # self.speed = self.prev_speed
        # self.prev_speed = 0