import random
import pygame
from Entities.enemy import zombie as enemy
import copy

class roomv2:
    def __init__(self, designation, x,y, paths, map = None, group = pygame.sprite.Group(), entered = False):
        self.name = designation
        self.x = x
        self.y = y
        self.paths = paths
        self.map = map  # Avoid storing mutable default args
        self.Rconnected = False

        #room contents
        self.interacted = False
        self.lootOrMonster = False
        self.entered = entered
        self.quantity = 2
        self.EneGroup = pygame.sprite.Group()
        self.EntGrp = pygame.sprite.Group()
        
        self.exit = False

        if self.lootOrMonster == True:
            for i in range(self.quantity):
                newEnem = enemy(i*40 + 80,320//x)
                self.EneGroup.add(newEnem)

        self.roomup =   None
        self.roomdown = None
        self.roomleft =  None
        self.roomright = None



    def Rconnect(self, themap):
        # Set self.map if not already set (using passed parameter)
        if self.map is None:
            self.map = themap
        
        # Connect room references
        if self.y > 0 and themap[self.y-1][self.x] is not None:
            self.roomup = themap[self.y-1][self.x]
        if self.y < len(themap)-1 and themap[self.y+1][self.x] is not None:
            self.roomdown = themap[self.y+1][self.x]
        if self.x > 0 and themap[self.y][self.x-1] is not None:
            self.roomleft = themap[self.y][self.x-1]
        if self.x < len(themap[0])-1 and themap[self.y][self.x+1] is not None:
            self.roomright = themap[self.y][self.x+1]

        # Fix the path multiplication logic:
        # If current room doesn't have path UP but room above has path DOWN, add path UP (2)
        if self.roomup is not None and not self.checkpath(2) and self.roomup.checkpath(3):
            self.paths = self.paths * 2
        
        # If current room doesn't have path DOWN but room below has path UP, add path DOWN (3)
        if self.roomdown is not None and not self.checkpath(3) and self.roomdown.checkpath(2):
            self.paths = self.paths * 3
        
        # If current room doesn't have path LEFT but room left has path RIGHT, add path LEFT (11)
        # Note: 11 = LEFT, so we multiply by 11
        if self.roomleft is not None and not self.checkpath(11) and self.roomleft.checkpath(7):
            self.paths = self.paths * 11
        
        # If current room doesn't have path RIGHT but room right has path LEFT, add path RIGHT (7)
        # Note: 7 = RIGHT, so we multiply by 7
        if self.roomright is not None and not self.checkpath(7) and self.roomright.checkpath(11):
            self.paths = self.paths * 7

        # Remove paths that lead out of bounds (use themap parameter)
        if self.checkpath(3) and self.y >= len(themap) - 1:  # DOWN path at bottom edge
            self.paths = int(self.paths // 3)
        elif self.checkpath(2) and self.y <= 0:  # UP path at top edge
            self.paths = int(self.paths // 2)
        
        if self.checkpath(7) and self.x >= len(themap[0]) - 1:  # RIGHT path at right edge
            self.paths = int(self.paths // 7)
        elif self.checkpath(11) and self.x <= 0:  # LEFT path at left edge
            self.paths = int(self.paths // 11)
        
        self.Rconnected = True
    
    def remove_path(self, prime):
        if self.paths % prime == 0:
            self.paths //= prime


    def spawnroom(self,roomtemplates, roomlist):
        room_up = None
        room_down = None
        room_right = None
        room_left = None
        # if the paths is divisible by 2, it has a path up
        # if the paths is divisible by 3, it has a path down
        # if the paths is divisible by 7, it has a path right
        # if the paths is divisible by 11, it has a path left
        if self.checkpath(2): # 2 divisibles for up
            if self.y > 0 and self.map[self.y-1][self.x] is None:
                tmpl = random.choice(roomtemplates.get("bottom"))
                room_up = roomv2(tmpl.name, self.x, self.y - 1, tmpl.paths, self.map)
                room_up.lootOrMonster = random.choice([True, False])
                room_up.quantity = tmpl.quantity
                self.map[room_up.y][room_up.x] = room_up
                self.map[room_up.y][room_up.x].spawnroom(roomtemplates, roomlist)

        if self.checkpath(3): # 3 divisibles for down
            if self.y < len(self.map)-1 and self.map[self.y + 1][self.x] is None:
                tmpl = random.choice(roomtemplates.get("top"))
                room_down = roomv2(tmpl.name, self.x, self.y + 1, tmpl.paths, self.map)
                room_down.lootOrMonster = random.choice([True, False])
                room_down.quantity = tmpl.quantity
                self.map[room_down.y][room_down.x] = room_down
                self.map[room_down.y][room_down.x].spawnroom(roomtemplates, roomlist)

        if self.checkpath(7): # 7 divisibles for right
            if self.x < len(self.map[0])-1 and self.map[self.y][self.x+1] is None:
                tmpl = random.choice(roomtemplates.get("right_exit"))
                room_right = roomv2(tmpl.name, self.x + 1, self.y, tmpl.paths, self.map)
                room_right.lootOrMonster = random.choice([True, False])
                room_right.quantity = tmpl.quantity
                self.map[room_right.y][room_right.x] = room_right
                self.map[room_right.y][room_right.x].spawnroom(roomtemplates, roomlist)

        if self.checkpath(11): # 11 divisibles for left
            if self.x > 0 and self.map[self.y][self.x-1] is None:
                tmpl = random.choice(roomtemplates.get("left_exit"))
                room_left = roomv2(tmpl.name, self.x - 1, self.y, tmpl.paths, self.map)
                room_left.lootOrMonster = random.choice([True, False])
                room_left.quantity = tmpl.quantity
                self.map[room_left.y][room_left.x] = room_left
                self.map[room_left.y][room_left.x].spawnroom(roomtemplates, roomlist)
        
        # After creating and adding a room, spawn its enemies
        if room_up:  # For upward room
            if room_up.lootOrMonster:
                room_up.spawn_enemies()
        
        if room_down:  # For downward room
            if room_down.lootOrMonster:
                room_down.spawn_enemies()
        
        if room_right:  # For rightward room
            if room_right.lootOrMonster:
                room_right.spawn_enemies()
        
        if room_left:  # For leftward room
            if room_left.lootOrMonster:
                room_left.spawn_enemies()
        roomlist.append(self)
    
    def checkpath(self, direction):
        if self.paths % direction == 0:
 
            return True

    def set_path(self, paths):
        self.paths = paths

    def __str__(self):
        return f"{self.name}"
    
    def spawn_enemies(self):
        """Spawn enemies for this room if lootOrMonster is True"""
        if self.lootOrMonster and self.quantity > 0:
            # Clear any existing enemies
            self.EneGroup.empty()
            
            # Spawn new enemies
            for i in range(self.quantity):
                # Fixed spawn positions (not dependent on x to avoid division by zero)
                spawn_x = 100 + (i * 60)  # Spread horizontally
                spawn_y = 160  # Middle of room
                new_enemy = enemy(spawn_x, spawn_y)
                self.EneGroup.add(new_enemy)
