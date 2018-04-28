import math

import inference_engine.light_deductive as light_deductive
import graphic.maps as maps
import pygame
from graphic.maps import MAP_NAVS, TRAFFIC_LAMP_POS

from graphic.loader import load_image
from inference_engine import impediment_deductive

PI = math.pi
max_a = 0.1

# define car as Player
class Car(pygame.sprite.Sprite):
    # init_x, init_y: center of image
    def __init__(self, init_x, init_y, init_after_x, init_after_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("car_player3.png")
        self.rect = self.image.get_rect()
        self.x = round(init_x, 1)
        self.y = round(init_y, 1)
        self.x_before = round(init_x, 1)
        self.y_before = round(init_y, 1)
        self.rect.topleft = init_x, init_y
        self.dir = 180 + calculate_dir(round(self.x, 1),round(self.y, 1),
                                    round(self.x_before, 1), round(self.y_before, 1),
                                    round(init_after_x, 1), round(init_after_y, 1))
        self.image, self.rect = rot_center(self.image, self.rect, self.dir)
        #Do dai dich chuyen
        self.add_van_toc_x = 0.1
        self.add_van_toc_y = 0.1
        self.initArray = 1

    def update(self, route):
        if(self.x == route[self.initArray][0] and self.y == route[self.initArray][1]):
            if (len(route) == self.initArray + 1):
                return
            else:
                self.initArray = self.initArray + 1
                dir = calculate_dir(round(self.x, 1),round(self.y, 1),
                                    round(self.x_before, 1), round(self.y_before, 1),
                                    round(route[self.initArray][0], 1), round(route[self.initArray][1], 1))
                self.image = pygame.transform.rotate(self.image, dir)
                if(self.initArray == 3 or self.initArray == 5 or self.initArray == 7):
                    self.add_van_toc_x = 0.2
                    self.add_van_toc_y = 0.2
                else:
                    self.add_van_toc_x = 0.1
                    self.add_van_toc_y = 0.1

        print(self.x, self.y)
        print(self.initArray)
        print(len(route))
        self.x_before, self.y_before = self.x, self.y
        self.x, self.y = self.calculate_van_toc(route[self.initArray][0], route[self.initArray][1])
        self.x, self.y = round(self.x, 1), round(self.y, 1)
        self.rect.topleft = self.x, self.y

    def calculate_van_toc(self, target_x, target_y):
        if ( (self.x == target_x) and (self.y < target_y) ):
            return self.x, self.y + self.add_van_toc_y
        if ( (self.x == target_x) and (self.y > target_y) ):
            return self.x, self.y + (-1)*self.add_van_toc_y
        if ( (self.x < target_x ) and (self.y == target_y)):
            return self.x + self.add_van_toc_x, self.y
        if ( (self.x > target_x) and (self.y == target_y) ):
            return self.x + (-1)*self.add_van_toc_x, self.y

def calculate_dir(current_x, current_y, before_x, before_y, target_x, target_y):
    # Di tu tren xuong duoi
    if (before_x == current_x and before_y == current_y):
        # Di tu trai qua phai
        if (current_x < target_x and current_y == target_y):
            return 90
        # Di tu phai qua trai
        if (current_x > target_x and current_y == target_y):
            return 270

    # Di tu tren xuong duoi
    if (before_x == current_x and before_y < current_y):
        # Di tu tren xuong tiep
        if (current_x == target_x and current_y < target_y):
            return 0
        # Di tu duoi len tren
        if (current_x == target_x and current_y > target_y):
            return 180
        # Di tu trai qua phai
        if (current_x < target_x and current_y == target_y):
            return 90
        # Di tu phai qua trai
        if (current_x > target_x and current_y == target_y):
            return 270

    # Di tu duoi len tren
    if (before_x == current_x and before_y > current_y):
        # Di tu tren xuong duoi
        if (current_x == target_x and current_y < target_y):
            return 180
        # Di tu duoi len tren tiep
        if (current_x == target_x and current_y > target_y):
            return 0
        # Di tu trai qua phai
        if (current_x < target_x and current_y == target_y):
            return 270
        # Di tu phai qua trai
        if (current_x > target_x and current_y == target_y):
            return 90

    # Di tu trai qua phai
    if (before_x < current_x and before_y == current_y):
        # Di tu trai qua
        if (current_x < target_x and current_y == target_y):
            return 0
        # Di tu phai qua
        if (current_x > target_x and current_y == target_y):
            return 180
        # Di tu tren xuong duoi
        if (current_x == target_x and current_y < target_y):
            return 270
        # Di tu duoi len tren
        if (current_x == target_x and current_y > target_y):
            return 90

    # Di tu Phai qua trai
    if (before_x > current_x and before_y == current_y):
        # Di tu Trai qua
        if (current_x < target_x and current_y == target_y):
            return 180
        # Di tu phai qua
        if (current_x > target_x and current_y == target_y):
            return 0
        # Di tu tren xuong duoi
        if (current_x == target_x and current_y < target_y):
            return 90
        # Di tu duoi len tren
        if (current_x == target_x and current_y > target_y):
            return 270

    return 0



def rot_center(image, rect, angle):
    """rotate an image while keeping itscenter"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect
def calculate_angle(point_x, point_y, target_x, target_y):
    neg_dir = math.atan2(point_y - target_y, target_x - point_x) * 180 / PI
    if neg_dir < 0:
        neg_dir += 360
    if neg_dir < 90:
        dir = neg_dir + 360 - 90
    else:
        dir = neg_dir - 90
    return dir
def calculate_abs_angle(point_x, point_y, target_x, target_y):
    dir = math.atan2(point_y - target_y, target_x - point_x) * 180 / PI
    return dir



