import pygame
from Entities.Player import Player_Character 
import math

class zombie(pygame.sprite.Sprite):
    def __init__(self, x , y, health = 10, speed = 1, group = None):
        super().__init__()
        pygame.init()
        self.img = pygame.image.load("Images/enemy_zombie.png")
        self.image = pygame.transform.smoothscale(self.img,(50,50))
        self.rect = self.image.get_rect(center = (x,y))
        self.health = health
        self.group = group
        self.speed = speed
        self.player =   Player_Character((0,0))  # Placeholder, will be set later}

        
    def update(self):
        if self.health <= 0:
            self.group.remove(self)
    
    def move_towards_player(self):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed