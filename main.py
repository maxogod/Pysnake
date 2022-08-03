import pygame
from pygame.locals import *
import time
import random
SIZE = 40

class Snake:
    def __init__(self, parent_screen, length) -> None:
        self.parent_screen = parent_screen
        self.snake_block = pygame.image.load("resources/snake_body.jpg").convert()
        self.length = length
        self.x = [SIZE] * self.length
        self.y = [SIZE] * self.length
        self.walk_direction = 'down'
	
    def draw(self):
        self.parent_screen.fill((37, 171, 123))
        for i in range(self.length):
            self.parent_screen.blit(self.snake_block, (self.x[i], self.y[i]))
        pygame.display.flip()
        
    def move(self, direction):
        self.direction = direction
        directions = {K_UP: 'up', K_DOWN: 'down', K_RIGHT: 'right', K_LEFT: 'left'}
        self.walk_direction = directions[self.direction]
        
    def walk(self):
        directionsy = {'up': - SIZE, 'down': SIZE}
        directionsx = {'right': SIZE, 'left': - SIZE}
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.walk_direction in directionsx:
            self.x[0] += directionsx[self.walk_direction]
        else:
            self.y[0] += directionsy[self.walk_direction]
        self.draw()


class Apple:
    def __init__(self, parent_screen) -> None:
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = random.randint(0, 18) * SIZE
        self.y = random.randint(0, 13) * SIZE
    
    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((37, 171, 123))
        self.snake = Snake(self.screen, 5)
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
                        if pygame.key.get_pressed()[i] and not game.check_180_degrees(i):
                            self.snake.move(i)
            self.snake.walk()
            self.apple.draw()
            time.sleep(.09)
    
    def check_180_degrees(self, key):
        boolean = False
        if key == K_UP and self.snake.walk_direction == 'down':
            boolean = True
        elif key == K_DOWN and self.snake.walk_direction == 'up':
            boolean = True
        elif key == K_RIGHT and self.snake.walk_direction == 'left':
            boolean = True
        elif key == K_LEFT and self.snake.walk_direction == 'right':
            boolean = True            
        return boolean


if __name__ == '__main__':
    game = Game()
    game.run()
