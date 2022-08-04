import pygame
from pygame.locals import *
import random
SIZE = (40)

class Snake:
    def __init__(self, parent_screen, length) -> None:
        self.parent_screen = parent_screen
        self.snake_block = pygame.image.load("resources/snake_body.jpg").convert()
        self.snake_head = pygame.image.load("resources/snake_head.jpg").convert()
        
        self.length = length
        self.x = [SIZE] * self.length
        self.y = [SIZE] * self.length
        
        self.walk_direction = 'down'
	
    def draw(self):
        self.parent_screen.blit(self.snake_head, (self.x[0], self.y[0]))
        for i in range(1, self.length):
            self.parent_screen.blit(self.snake_block, (self.x[i], self.y[i]))
        
    def move(self, direction):
        directions = {K_UP: 'up', K_DOWN: 'down', K_RIGHT: 'right', K_LEFT: 'left'}
        self.walk_direction = directions[direction]
        
    def walk(self):
        directionsy = {'up': - SIZE, 'down': SIZE}
        directionsx = {'right': SIZE, 'left': - SIZE}
        
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.walk_direction in directionsx:
            self.x[0] += directionsx[self.walk_direction]
        else:
            self.y[0] += directionsy[self.walk_direction]
        self.draw()
        
    def increase_length(self):
        self.length += 1
        self.x.append(SIZE)
        self.y.append(SIZE)
        
    def collision_check(self):
        boolean = True
        if self.length > 1:
            pos = 1
            while pos < self.length:
                if self.x[0] == self.x[pos] and self.y[0] == self.y[pos]:
                    boolean = False
                pos += 1
                
        if boolean and ((self.x[0] >= 800 or self.x[0] < 0)
                        or (self.y[0] >= 600 or self.y[0] < 0)):
            boolean = False
            
        return boolean
    
    def check_180_degrees(self, key):
        boolean = False
        if key == K_UP and self.walk_direction == 'down':
            boolean = True
        elif key == K_DOWN and self.walk_direction == 'up':
            boolean = True
        elif key == K_RIGHT and self.walk_direction == 'left':
            boolean = True
        elif key == K_LEFT and self.walk_direction == 'right':
            boolean = True            
        return boolean


class Apple:
    def __init__(self, parent_screen) -> None:
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.png").convert_alpha()
        
        self.x = random.randint(0, 18) * SIZE
        self.y = random.randint(0, 13) * SIZE
    
    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        
    def change_pos(self, snake_x, snake_y):
        new_x = random.randint(0, 18) * SIZE
        new_y = random.randint(0, 13) * SIZE
        while new_x in snake_x or new_y in snake_y:
            new_x = random.randint(0, 18) * SIZE
            new_y = random.randint(0, 13) * SIZE
        self.x = new_x
        self.y = new_y