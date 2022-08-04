import pygame
from pygame.locals import *
import time
import objects

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('PYSNAKE by maxogod')
        self.icon = pygame.image.load('resources/icon.ico').convert()
        pygame.display.set_icon(self.icon)
        self.grass = pygame.image.load("resources/grass.jpg").convert()
        
        self.snake = objects.Snake(self.screen, 1)
        self.snake.draw()
        self.apple = objects.Apple(self.screen)
        self.apple.draw()
        
    def run(self):
        running = True
        start = True
        while running:
            
            if start:
                self.title()
                self.play_audio_file('music_tittle')
                while not (pygame.key.get_pressed()[K_ESCAPE] or pygame.key.get_pressed()[K_KP_ENTER]
                           or not start):
                    for event in pygame.event.get():
                        if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:
                            exit(0)
                        elif pygame.key.get_pressed()[K_SPACE]:
                            start = False
                            self.play_audio_file('music_game')
                            
            for event in pygame.event.get():
                if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:
                    running = False
                elif pygame.key.get_pressed():
                    for i in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                        if pygame.key.get_pressed()[i] and not self.snake.check_180_degrees(i):
                            self.snake.move(i)
                            
            self.screen.blit(self.grass, (0, 0))               
            self.snake.walk()
            
            if not self.snake.collision_check():
                self.play_audio_file('sound_crash')
                self.play_audio_file('music_gameover')
                
                hscore = self.highscore_check()
                self.gameover(hscore)
                
                while not (pygame.key.get_pressed()[K_ESCAPE] or pygame.key.get_pressed()[K_SPACE]
                           or event.type == QUIT):
                    for event in pygame.event.get():
                        if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:
                            exit(0)
                        elif pygame.key.get_pressed()[K_SPACE]:
                            self.reinitialize()
                            self.play_audio_file('music_game')
                            
            self.apple_collision_check()
            self.apple.draw()
            self.score()
            pygame.display.flip()
            time.sleep(.09)
    
    def play_audio_file(self, use):
        songs_and_sounds = {
            'music_tittle': ('resources/tittle_music.mp3', 0.1),
            'music_game': ('resources/game_music.mp3', 0.05),
            'music_gameover': ('resources/gameover_music.mp3', 0.02),
            'sound_eat': ('resources/eats.mp3', 0.07),
            'sound_crash': ('resources/crash.mp3', 0.07)
        }
        
        if use.startswith('music'):
            pygame.mixer.music.unload()
            pygame.mixer.music.set_volume(songs_and_sounds[use][1])
            pygame.mixer.music.load(songs_and_sounds[use][0])
            pygame.mixer.music.play()
            
        elif use.startswith('sound'):
            sound = pygame.mixer.Sound(songs_and_sounds[use][0])
            pygame.mixer.Sound.set_volume(sound, songs_and_sounds[use][1])
            pygame.mixer.Sound.play(sound)
    
    def title(self):
        self.title_img = pygame.image.load("resources/title.jpg").convert()
        self.screen.blit(self.title_img, (0, 0))
        pygame.display.flip()
        
    def reinitialize(self):
        self.screen.blit(self.grass, (0, 0))
        self.snake = objects.Snake(self.screen, 1)
        self.snake.draw()
        self.apple = objects.Apple(self.screen)
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
    
    def apple_collision_check(self):
        if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
            self.play_audio_file('sound_eat')
            self.snake.increase_length()
            self.apple.change_pos(self.snake.x, self.snake.y)
    
    def score(self):
        font = pygame.font.SysFont('arial', 40)
        score = font.render(f'Score: {self.snake.length}', True, (255, 255, 255))
        self.screen.blit(score, (650, 550))
     

if __name__ == '__main__':
    game = Game()
    game.run()
