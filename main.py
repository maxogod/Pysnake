from turtle import Screen
import pygame
from pygame.locals import *
import time

class Snake:
    
    def __init__(self, parent_screen) -> None:
        self.parent_screen = parent_screen
        self.snake_block = pygame.image.load("resources/snake_body.jpg").convert()
        self.x = 500
        self.y = 400
        self.walk_direction = 'down'
	
    def draw(self):
        self.parent_screen.fill((37, 171, 123))
        self.parent_screen.blit(self.snake_block, (self.x, self.y))
        pygame.display.flip()
        
    def move(self, direction):
        self.direction = direction
        directions = {K_UP: 'up', K_DOWN: 'down', K_RIGHT: 'right', K_LEFT: 'left'}
        self.walk_direction = directions[self.direction]
        
    def walk(self):
        directionsy = {'up': -10, 'down': 10}
        directionsx = {'right': 10, 'left': -10}
        if self.walk_direction in directionsx:
            self.x += directionsx[self.walk_direction]
        else:
            self.y += directionsy[self.walk_direction]
        self.draw()


class Apple:
    
    def __init__(self, parent_screen) -> None:
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = 100
        self.y = 100
    
    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()


class Game:
    
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((37, 171, 123))
        self.snake = Snake(self.screen)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()
        
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:
                    running = False
                elif pygame.key.get_pressed():
                    for i in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                        if pygame.key.get_pressed()[i]:
                            self.snake.move(i)
            self.snake.walk()
            self.apple.draw()
            time.sleep(.07)
                            

if __name__ == '__main__':
    game = Game()
    game.run()
