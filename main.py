import pygame
from pygame.locals import *
import time
import random
SIZE = 40

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
        self.direction = direction
        directions = {K_UP: 'up', K_DOWN: 'down', K_RIGHT: 'right', K_LEFT: 'left'}
        self.walk_direction = directions[self.direction]
        
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


class Game:
    def __init__(self) -> None:
        pygame.init()
        
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.1)
        
        self.screen = pygame.display.set_mode((800, 600))
        self.grass = pygame.image.load("resources/grass.jpg").convert()
        self.snake = Snake(self.screen, 1)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()
        
    def run(self):
        running = True
        start = True
        while running:
            if start:
                self.title()
                pygame.mixer.music.load('resources/tittle_music.mp3')
                pygame.mixer.music.play()
                while not (pygame.key.get_pressed()[K_ESCAPE] or pygame.key.get_pressed()[K_KP_ENTER]
                           or not start):
                    for event in pygame.event.get():
                        if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:
                            exit(0)
                        elif pygame.key.get_pressed()[K_SPACE]:
                            start = False
                            pygame.mixer.music.unload()
                            pygame.mixer.music.set_volume(0.05)
                            pygame.mixer.music.load('resources/game_music.mp3')
                            pygame.mixer.music.play()
            for event in pygame.event.get():
                if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:
                    running = False
                elif pygame.key.get_pressed():
                    for i in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                        if pygame.key.get_pressed()[i] and not game.check_180_degrees(i):
                            self.snake.move(i)
            self.screen.blit(self.grass, (0, 0))               
            self.snake.walk()
            if not self.snake_collision_check():
                crash = pygame.mixer.Sound('resources/crash.mp3')
                pygame.mixer.Sound.set_volume(crash, 0.07)
                pygame.mixer.Sound.play(crash)
                pygame.mixer.music.unload()
                pygame.mixer.music.set_volume(0.02)
                pygame.mixer.music.load('resources/gameover_music.mp3')
                pygame.mixer.music.play()
                hscore = self.highscore_check()
                self.gameover(hscore)
                while not (pygame.key.get_pressed()[K_ESCAPE] or pygame.key.get_pressed()[K_SPACE]
                           or event.type == QUIT):
                    for event in pygame.event.get():
                        if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:
                            exit(0)
                        elif pygame.key.get_pressed()[K_SPACE]:
                            self.reinitialize()        
            self.apple_collision_check()
            self.apple.draw()
            self.score()
            pygame.display.flip()
            time.sleep(.09)
    
    def title(self):
        self.title_img = pygame.image.load("resources/title.jpg").convert()
        self.screen.blit(self.title_img, (0, 0))
        pygame.display.flip()
        
    def reinitialize(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((37, 171, 123))
        self.snake = Snake(self.screen, 1)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()
    
    def gameover(self, hscore):
        self.dead = pygame.image.load("resources/dead.jpg").convert()
        font = pygame.font.SysFont('', 40)
        
        score = font.render(f'Your score: {self.snake.length}', True, (255, 255, 255))
        hscore_text = font.render(f'Highscore: {hscore}', True, (255, 255, 255))
        
        self.screen.blit(self.dead, (0, 0))
        self.screen.blit(score, (350, 320))
        self.screen.blit(hscore_text, (350, 380))
        pygame.display.flip()
        
    def highscore_check(self):
        score = self.snake.length
        with open('resources/highscore.csv', 'r') as hscore:
            try:
               hscore_content = int(hscore.readline().rstrip('\n'))
            except ValueError:
                hscore_content = 0
        if score > hscore_content:
            with open('resources/highscore.csv', 'w') as hscore:
                hscore.write(str(score))
                return score
        return hscore_content
    
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
    
    def snake_collision_check(self):
        boolean = True
        if self.snake.length > 1:
            pos = 1
            while pos < self.snake.length:
                if self.snake.x[0] == self.snake.x[pos] and self.snake.y[0] == self.snake.y[pos]:
                    boolean = False
                pos += 1
                
        if boolean and (self.snake.x[0] >= 800 or self.snake.x[0] < 0) or (self.snake.y[0] >= 600 or self.snake.y[0] < 0):
            boolean = False
        return boolean
    
    def apple_collision_check(self):
        if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
            eats = pygame.mixer.Sound('resources/eats.mp3')
            pygame.mixer.Sound.set_volume(eats, 0.07)
            pygame.mixer.Sound.play(eats)
            self.snake.increase_length()
            self.apple.change_pos(self.snake.x, self.snake.y)
    
    def score(self):
        font = pygame.font.SysFont('arial', 40)
        score = font.render(f'Score: {self.snake.length}', True, (255, 255, 255))
        self.screen.blit(score, (650, 550))
     

if __name__ == '__main__':
    game = Game()
    game.run()
