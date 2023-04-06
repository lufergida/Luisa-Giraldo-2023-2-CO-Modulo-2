import pygame
import random

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE

class PowerUpManager:
  def __init__(self):
    self.power_ups = []
    self.duration = random.randint(3, 5)
    #self.when_appears = random.randint(50, 70)
    self.countdown = 0
    
  def update(self, game):
    if len(self.power_ups) == 0 and self.countdown == 0:
      self.generate_power_up()
      self.countdown = random.randint(200, 300)
    else:
      self.countdown -= 1
    if self.countdown == 0:
      self.generate_power_up()
      self.countdown = random.randint(200, 300)
    for power_up in self.power_ups:
      power_up.update(game.game_speed, self.power_ups)
      if game.player.dino_rect.colliderect(power_up.rect):
          #Formula del tiempo
          power_up.start_time = pygame.time.get_ticks()
          game.player.has_power_up = True
          if power_up.type == SHIELD_TYPE:
              game.player.type = SHIELD_TYPE
          elif power_up.type == HAMMER_TYPE:
              game.player.type = HAMMER_TYPE
          game.player.power_up_time = power_up.start_time + (self.duration * 1000)
          self.power_ups.remove(power_up)

    
  def draw(self, screen):
    for power_up in self.power_ups:
      power_up.draw(screen)
    
  def reset_power_ups(self):
   self.power_ups= []
   #self.when_appears= random.randint(50, 70)
    
  def generate_power_up(self):
    power_up_type = random.choice([SHIELD_TYPE, HAMMER_TYPE])
    if power_up_type == SHIELD_TYPE:
        power_up = Shield()
    elif power_up_type == HAMMER_TYPE:
        power_up = Hammer()
    self.power_ups.append(power_up)

        
        