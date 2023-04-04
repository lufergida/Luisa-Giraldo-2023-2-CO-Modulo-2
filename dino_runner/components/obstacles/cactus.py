import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Cactus(Obstacle):
# Image es una lista
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        
#    def draw(self, screen):
#        screen.blit(self.image[self.obstacle_type], (self.rect.x, self.rect.y))
        
    
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300