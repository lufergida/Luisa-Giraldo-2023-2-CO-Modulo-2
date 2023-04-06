import random
import pygame

from dino_runner.components import obstacles
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cloud import Cloud
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, CLOUD, SHIELD_TYPE, HAMMER_TYPE


class ObstacleManager:
  def __init__(self):
    self.obstacles = []
    self.cloud = self.generate_cloud()

  def update(self, game):
    if len(self.obstacles) == 0:
      obstacle = self.generate_obstacle(random.randint(0,2))
      self.obstacles.append(obstacle)

    for obstacle in self.obstacles:
      obstacle.update(game.game_speed, self.obstacles)
      if game.player.dino_rect.colliderect(obstacle.rect):
        if game.player.type != SHIELD_TYPE:
          game.playing = False
          game.death_count += 1
          break
        else:
          self.obstacles.remove(obstacle)
      if game.player.type == HAMMER_TYPE and pygame.key.get_pressed()[pygame.K_SPACE]:
        if obstacle.rect.colliderect(game.player.hammer_rect):
          self.obstacles.remove(obstacle)

    self.cloud.update(game.game_speed)


  def draw(self, screen):
    for obstacle in self.obstacles:
      obstacle.draw(screen)

    self.cloud.draw(screen)

  def generate_obstacle(self, obstacle_type):
    if obstacle_type == 0:
      cactus_type = 'SMALL'
      obstacle = Cactus(cactus_type)
    elif obstacle_type == 1:
      cactus_type = 'LARGE'
      obstacle = Cactus(cactus_type)
    else:
      obstacle = Bird()
    return obstacle

  def generate_cloud(self):
    return Cloud()

  def reset_obstacles(self):
    self.obstacles = []
