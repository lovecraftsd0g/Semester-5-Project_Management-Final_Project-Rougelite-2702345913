import pygame

class portal(pygame.sprite.Sprite):
    def __init__(self,pos = (50,50)):
        super().__init__()
        pygame.init()
        self.img1 = pygame.image.load("Images/portal.png")
        self.img2 = pygame.image.load("Images/portal2.png")
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.imgsurf = pygame.transform.smoothscale(self.img1, (50,50))
        self.image = self.imgsurf  # Required for pygame sprite drawing
        self.rect = self.image.get_rect(center = (self.xpos,self.ypos))
        self.active = False
    def update(self, value, reqVal):
        if value >= reqVal:
            self.imgsurf = pygame.transform.smoothscale(self.img2, (50,50))
            self.image = self.imgsurf  # Required for pygame sprite drawing
            self.rect = self.image.get_rect(center = (self.xpos,self.ypos))
        else:
            self.imgsurf = pygame.transform.smoothscale(self.img1, (50,50))
            self.image = self.imgsurf  # Required for pygame sprite drawing
            self.rect = self.image.get_rect(center = (self.xpos,self.ypos))