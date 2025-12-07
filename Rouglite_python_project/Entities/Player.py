import pygame
from roomStuff.tiles import tile as t

class Player_Character(pygame.sprite.Sprite):
    def __init__(self, pos, colGroups = None,speed = 3,projectiles = None, attack_rad = 5):
        super().__init__()  # Initialize the parent Sprite class
        pygame.init()
        img = pygame.image.load("Images/Player.png")  # Use forward slash for paths
        self.image = pygame.transform.smoothscale(img,(50,50))
        self.rect = self.image.get_rect(center = pos)

        #player health, player has knife, instead of life
        self.knife = 3

        #attack radius
        self.attack_rad = attack_rad
        self.atkm = False
        self.targetI = 0
        
        # movement
        self.blocks = colGroups
        self.speed = speed
        self.colliding = 1
        self.velx = 0
        self.vely = 0

    def update(self):
        # Reset velocity at the start of each frame
        self.velx = 0
        self.vely = 0
        
        keys = pygame.key.get_pressed()
        
        # Handle input first
        if not self.atkm:
            if keys[pygame.K_w]:
                self.vely = -self.speed
            elif keys[pygame.K_s]:
                self.vely = self.speed
            if keys[pygame.K_a]:
                self.velx = -self.speed
            elif keys[pygame.K_d]:
                self.velx = self.speed
                
        # Check collision before applying movement
        self.checkCol()
        
        # Apply movement based on collision state
        if self.velx < 0 and self.colliding % 2 != 0:  # Moving left and no left collision
            self.rect.centerx += self.velx
        elif self.velx > 0 and self.colliding % 3 != 0:  # Moving right and no right collision
            self.rect.centerx += self.velx
            
        if self.vely < 0 and self.colliding % 5 != 0:  # Moving up and no top collision
            self.rect.centery += self.vely
        elif self.vely > 0 and self.colliding % 7 != 0:  # Moving down and no bottom collision
            self.rect.centery += self.vely

    def checkCol(self):
        self.colliding = 1
        
        if not self.blocks:
            return
            
        # Get all sprites from the group and check each one
        for tile in self.blocks.sprites():
            # Check if the tile is meant to be collidable
            if not tile.returncol():
                continue
            
            # Get the rectangles for collision checking
            player_rect = self.rect
            tile_rect = tile.returnrect()
            
            # Calculate the overlap
            overlap_x = min(player_rect.right, tile_rect.right) - max(player_rect.left, tile_rect.left)
            overlap_y = min(player_rect.bottom, tile_rect.bottom) - max(player_rect.top, tile_rect.top)
            
            # If there's no overlap, skip this tile
            if overlap_x <= 0 or overlap_y <= 0:
                continue
                
            # Determine which side the collision is occurring on
            collision_tolerance = 10  # Adjust this value if needed
            
            # Left collision
            if abs(tile_rect.right - player_rect.left) < collision_tolerance:
                self.colliding *= 2  # Left collision flag
            
            # Right collision
            if abs(tile_rect.left - player_rect.right) < collision_tolerance:
                self.colliding *= 3  # Right collision flag
            
            # Top collision
            if abs(tile_rect.bottom - player_rect.top) < collision_tolerance:
                self.colliding *= 5  # Top collision flag
            
            # Bottom collision
            if abs(tile_rect.top - player_rect.bottom) < collision_tolerance:
                self.colliding *= 7  # Bottom collision flag
    
    def collisonCheck(self, colNumber):
        if self.colliding % colNumber == 0:
            return True
        else:
            return False
                    

#hit scan
class Atk(pygame.sprite.Sprite):
    def __init__(self, pos, entity_targets, Size=(50, 50), damage=20):
        super().__init__()  # Fixed syntax
        # Use SRCALPHA surface so semi-transparency works
        self.image = pygame.Surface(Size, pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 128))  # Semi-transparent red
        self.rect = self.image.get_rect(center=pos)
        self.index = 0
        self.targlis = []
        self.entity_targets = entity_targets
        self.damage = damage
        self.active = False

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Clear and update target list
        self.targlis = []
        for entity in self.entity_targets:
            if self.rect.colliderect(entity.rect):
                self.targlis.append(entity)
        
        # Handle attack
        if keys[pygame.K_x] and len(self.targlis) > 0:
            if self.index < len(self.targlis):  # Make sure index is valid
                target = self.targlis[self.index]
                if hasattr(target, 'health'):  # Check if target has health attribute
                    target.health -= self.damage

                
