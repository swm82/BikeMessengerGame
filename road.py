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
        self.pavement.fill(Road.pavement_color)
        # road_objects.append(road)

        self.line_thickness = self.road_size[1]/80

        # Yellow centerlines
        self.centerline = pygame.Surface((self.screen_width, self.line_thickness))
        self.centerline.fill(Road.centerline_color)

        # Lane line
        self.lane_line_surface = pygame.Surface((50, self.line_thickness))
        self.lane_line_surface.fill((255, 255, 255))
        # self.rect = self.surface.get_rect()


    def draw_road(self):
        center_of_screen = self.screen_height / 2 
        # Top of road is 1/4 of way from top of screen
        top_of_road = center_of_screen/2

        self.screen.blit(self.pavement, (0, top_of_road))

        self.screen.blit(self.centerline, (0, center_of_screen - self.screen_height/150))
        self.screen.blit(self.centerline, (0, center_of_screen + self.screen_height/150))

        
        width_of_half_road = self.road_size[1]/2
        num_lane_lines = 10
        lane_spacing = self.lane_line_surface.get_width()
        
        for side_of_road in range(2):
            for lane in range(1,self.num_lanes):
                # draw lanes across screen
                for line in range(num_lane_lines):
                    # offset from x = 0
                    x_offset = self.lane_line_surface.get_width()*line + line*lane_spacing
                    y_offset = top_of_road + ((width_of_half_road/self.num_lanes)*lane) + side_of_road*(self.road_size[1]/2) - self.line_thickness
                    self.screen.blit(self.lane_line_surface, (x_offset, y_offset))

    def get_dimensions(self):
        return self.road_size

    def get_car_y_coords(self):
        center_of_screen = self.screen_height / 2 
        top_of_road = center_of_screen/2
        # TODO: Handle spacing within the lane (10*line_thickness)
        return [top_of_road + (i*(self.road_size[1]/(self.num_lanes*2))) - 10*self.line_thickness for i in range(1,2*self.num_lanes+1)]