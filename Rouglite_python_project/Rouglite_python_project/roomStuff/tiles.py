from pygame import *
import pygame

class tile(sprite.Sprite):
    def __init__(self, image, pos, collideble = False):
        super().__init__()  # Initialize the parent Sprite class
        pygame.init()
        self.img = pygame.image.load(image)
        self.image = pygame.transform.smoothscale(self.img, (32,32))
        self.rect = self.image.get_rect(center = pos)
        self.collideble = collideble
        self.index_X = pos[0]//32
        self.index_Y = pos[1]//32
    
    def returnpos(self):
        return [self.rect.centerx, self.rect.centery]
    def returnrect(self):
        return self.rect
    def returncol(self):
        return self.collideble