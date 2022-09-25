import pygame
from pygame.locals import *
import random
from constants import *


class Snake:
    def __init__(self, parent_screen, length) -> None:
        self.parent_screen = parent_screen
        self.snake_block = pygame.image.load("resources/snake_body.jpg").convert()
        self.snake_head = pygame.image.load("resources/snake_head.jpg").convert()
        
        self.length = length
        self.x = [BLOCK_SIZE] * self.length
        self.y = [BLOCK_SIZE] * self.length
        
        self.walk_direction = K_DOWN

    def draw(self):
        self.parent_screen.blit(self.snake_head, (self.x[HEAD_INDEX], self.y[HEAD_INDEX]))
        for body_block in range(1, self.length):
            self.parent_screen.blit(self.snake_block, (self.x[body_block], self.y[body_block]))

    def move(self, direction):
        if not self.__check_180_degrees(direction):
            self.walk_direction = direction
        
    def walk(self):
        directions_y = {K_UP: - BLOCK_SIZE, K_DOWN: BLOCK_SIZE}
        directions_x = {K_RIGHT: BLOCK_SIZE, K_LEFT: - BLOCK_SIZE}
        
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.walk_direction in directions_x:
            self.x[HEAD_INDEX] += directions_x[self.walk_direction]
        else:
            self.y[HEAD_INDEX] += directions_y[self.walk_direction]
        self.draw()
        
    def increase_length(self):
        self.length += 1
        self.x.append(BLOCK_SIZE)
        self.y.append(BLOCK_SIZE)
        
    def collision_check(self):
        boolean = True
        __START_OF_SCREEN = 0

        if self.length > 1:
            pos = 1
            while pos < self.length:
                if self.x[HEAD_INDEX] == self.x[pos] and self.y[HEAD_INDEX] == self.y[pos]:
                    boolean = False
                pos += 1
                
        if boolean and ((self.x[HEAD_INDEX] >= SCREEN_HEIGHT or self.x[HEAD_INDEX] < __START_OF_SCREEN)
                        or (self.y[HEAD_INDEX] >= SCREEN_WIDTH or self.y[HEAD_INDEX] < __START_OF_SCREEN)):
            boolean = False
            
        return boolean
    
    def __check_180_degrees(self, key):
        boolean = False
        if key == K_UP and self.walk_direction == K_DOWN:
            boolean = True
        elif key == K_DOWN and self.walk_direction == K_UP:
            boolean = True
        elif key == K_RIGHT and self.walk_direction == K_LEFT:
            boolean = True
        elif key == K_LEFT and self.walk_direction == K_RIGHT:
            boolean = True            
        return boolean


class Apple:
    def __init__(self, parent_screen) -> None:
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.png").convert_alpha()
        
        self.x = tp_to_random_place("x")
        self.y = tp_to_random_place("y")
    
    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        
    def change_pos(self, snake_x, snake_y):
        new_x = tp_to_random_place("x")
        new_y = tp_to_random_place("y")
        pos = 0
        while new_x == snake_x[pos] and new_y == snake_y[pos]:
            new_x = tp_to_random_place("x")
            new_y = tp_to_random_place("y")
            pos += 1
        self.x = new_x
        self.y = new_y


def tp_to_random_place(direction):
    max_factor = {"x": 18, "y": 13}
    return random.randint(0, max_factor[direction]) * BLOCK_SIZE
