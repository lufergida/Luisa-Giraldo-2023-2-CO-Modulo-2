import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.menu import Menu
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:
    GAME_SPEED = 20
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = self.GAME_SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.menu = Menu(self.screen, "Press any key to start...")
        self.running = False
        self.score = 0
        self.death_count = 0        
        self.max_score = 0
        self.power_up_manager = PowerUpManager()
        

    def run(self):
        self.playing = True
        self.reset_game()
        self.game_speed = self.GAME_SPEED
        self.score = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.score_status()   

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.score_status()
        self.draw_power_up()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed


    def show_menu(self):
        self.menu.reset_screen_color(self.screen)
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        self.screen.blit(ICON, (half_screen_width - 50, half_screen_height -140))
        if self.death_count == 0:
            self.menu.draw(self.screen, "Welcome to the game!")
        else:
            self.menu.update_message("")
            self.menu.draw(self.screen, f'Dino has died {self.death_count} times :(')
        self.menu.update(self)
        

    def score_status(self):
        self.score += 1
        if self.score % 200 == 0 and self.game_speed < 500:
            self.game_speed += 5
        if self.score > self.max_score:
            self.max_score = self.score      
        font = pygame.font.SysFont('Monospace', 30)
        text = font.render(f'Score: {self.score} | Max Score: {self.max_score}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (800, 50)
        self.screen.blit(text, text_rect)
    
    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.score = 0
        self.game_speed = self.GAME_SPEED
        self.player.reset()
        self.power_up_manager.reset_power_ups()
    
    def draw_power_up(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks())/1000,2)
            if time_to_show >= 0:
                self.menu.draw(self.screen, f'{self.player.type.capitalize()} enabled for {time_to_show} seconds', 550, 100)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
                

