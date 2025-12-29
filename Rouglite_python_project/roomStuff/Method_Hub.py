from roomStuff.room_stuff import roomv2 as room
from roomStuff.tiles import tile as t
import random
import pygame
from Entities.enemy import zombie




def generate_rooms(map, room_list):
    TBLR = room("TBLR",2,2,462,map)
    
    T =  room("T   ",0,0,2,map)
    B =  room(" B  ",0,0,3,map)
    L =  room("  L ",0,0,11,map)
    R =  room("   R",0,0,7,map)

    TB = room("TB  ",0,0,6,map)
    TR = room("T  R",0,0,14,map)
    TL = room("T L ",0,0,22,map)
    BR = room(" B R",0,0,21,map)
    BL = room(" BL ",0,0,33,map)

    room_templates = {
        "top": [T,TR,TL,TB],
        "bottom": [B,BR,BL,TB],
        "right_exit": [L,TL,BL,TB],
        "left_exit": [R,TR,BR,TB]
        }
    TBLR.x = 2
    TBLR.y  = 2
    map[2][2] = TBLR

    TBLR.spawnroom(room_templates, room_list)
    
    
    return room_list

def generateContents(r, player):
    if r.quantity > 0 and r.lootOrMonster:
        posxbas = 320//2
        posx = posxbas - 30
        for i in range(r.quantity):
            zom = zombie(posx + (i*30), 320//2)
            zom.player = player
            zom.group = r.group
            r.group.add(zom)

def generate_current_room_tiles(t_Grp, themap,x,y):
    left_door = [(0,3),(0,4),(0,5)]
    right_door = [(9,3),(9,4),(9,5)]
    top_door = [(3,0),(4,0),(5,0)]
    bottom_door = [(3,9),(4,9),(5,9)]

    all_door = [top_door, bottom_door, right_door, left_door]

    # get current room object (may be None)
    curr = themap[y][x]

    if curr is None:
        return

    if curr.paths % 2 == 0:
        for tile in t_Grp:
            if (tile.index_X, tile.index_Y) in all_door[0]:
                t_Grp.remove(tile)
    else:
        newtiles1 = t("Images/tiles/test_01.png", (3 * 32 + 16, 0 * 32 + 16), True)
        newtiles2 = t("Images/tiles/test_01.png", (4 * 32 + 16, 0 * 32 + 16), True)
        newtiles3 = t("Images/tiles/test_01.png", (5 * 32 + 16, 0 * 32 + 16), True)
        t_Grp.add(newtiles1, newtiles2, newtiles3)

    if curr.paths % 3 == 0:
        for tile in t_Grp:
            if (tile.index_X, tile.index_Y) in all_door[1]:
                t_Grp.remove(tile)
    else:
        newtiles1 = t("Images/tiles/test_01.png", (3 * 32 + 16, 9 * 32 + 16), True)
        newtiles2 = t("Images/tiles/test_01.png", (4 * 32 + 16, 9 * 32 + 16), True)
        newtiles3 = t("Images/tiles/test_01.png", (5 * 32 + 16, 9 * 32 + 16), True)
        t_Grp.add(newtiles1, newtiles2, newtiles3)

    if curr.paths % 7 == 0  :
        for tile in t_Grp:
            if (tile.index_X, tile.index_Y) in all_door[2]:
                t_Grp.remove(tile)
    else:
        newtiles1 = t("Images/tiles/test_01.png", (9 * 32 + 16, 3 * 32 + 16), True)
        newtiles2 = t("Images/tiles/test_01.png", (9 * 32 + 16, 4 * 32 + 16), True)
        newtiles3 = t("Images/tiles/test_01.png", (9 * 32 + 16, 5 * 32 + 16), True)
        t_Grp.add(newtiles1, newtiles2, newtiles3)

    if curr.paths % 11 == 0 :
        for tile in t_Grp:
            if (tile.index_X, tile.index_Y) in all_door[3]:
                t_Grp.remove(tile)
    else:
        newtiles1 = t("Images/tiles/test_01.png", (0 * 32 + 16, 3 * 32 + 16), True)
        newtiles2 = t("Images/tiles/test_01.png", (0 * 32 + 16, 4 * 32 + 16), True)
        newtiles3 = t("Images/tiles/test_01.png", (0 * 32 + 16, 5 * 32 + 16), True)
        t_Grp.add(newtiles1, newtiles2, newtiles3)

def run_game(player, tiles, clock, window, EnemyGroup, players, pAtkGroup, atk, Player_resources, entities, room_Score):
    #this is the hit scan script, drawn before the window.fill() function to put it waya from the eyes of the people
    pAtkGroup.draw(window)
    pAtkGroup.update()
    atk.rect.centerx = player.rect.centerx
    atk.rect.centery = player.rect.centery + 5


    window.fill((0,100,0))
    


    # draw the tiles first so entities render on top
    tiles.draw(window)

    #draw the player resources
    font = pygame.font.SysFont(None, 30)
    text = font.render(f'resource: {Player_resources}/2', True, (0, 255, 0))
    window.blit(text, (0,0))
    #draw the room score
    text2 = font.render(f'rooms cleared: {room_Score}/5', True, (0, 255, 0))
    window.blit(text2, (0, 30))
    # draw the entities
    entities.draw(window)
    EnemyGroup.draw(window)
    players.draw(window)
    EnemyGroup.update()

    entities.update(Player_resources, 2)
    players.update()

    pygame.display.update()
    clock.tick(60)
    
def makeenemymove(EnemyGroup):
    for enemy in EnemyGroup:
        enemy.move_towards_player()



def remove_improper_paths(themap, rooms):
    for r in rooms:

        # Top edge: no UP
        if r.y == 0:
            r.remove_path(2)

        # Bottom edge: no DOWN
        if r.y == len(themap) - 1:
            r.remove_path(3)

        # Right edge: no RIGHT
        if r.x == len(themap[0]) - 1:
            r.remove_path(7)

        # Left edge: no LEFT
        if r.x == 0:
            r.remove_path(11)

    for r in rooms:
        bol = [False, True]
        lom = random.randint(0,1)
        Amt = random.randint(1,2)
        r.entered = False
        r.interacted = False
        r.quantity = Amt
        r.lootOrMonster = bol[lom]



        #closes the rooms out at the edges of the map, and closes rooms that arent connected properly
        # Check UP connection
        if r.checkpath(2) and r.y > 0 and themap[r.y - 1][r.x] is not None:
            if not themap[r.y - 1][r.x].checkpath(3):  # Adjacent room doesn't have DOWN path
                r.remove_path(2)
                if r.roomup in rooms:
                    print(r.roomup.name)
                    rooms.remove(r.roomup)
        
        # Check DOWN connection
        if r.checkpath(3) and r.y < len(themap) - 1 and themap[r.y + 1][r.x] is not None:
            if not themap[r.y + 1][r.x].checkpath(2):  # Adjacent room doesn't have UP path
                r.remove_path(3)
                if r.roomdown in rooms:
                    print(r.roomdown.name)
                    rooms.remove(r.roomdown)
        
        # Check LEFT connection
        if r.checkpath(11) and r.x > 0 and themap[r.y][r.x - 1] is not None:
            if not themap[r.y][r.x - 1].checkpath(7):  # Adjacent room doesn't have RIGHT path
                r.remove_path(11)
                if r.roomleft in rooms:
                    print(r.roomleft.name)
                    rooms.remove(r.roomleft)
        
        # Check RIGHT connection
        if r.checkpath(7) and r.x < len(themap[0]) - 1 and themap[r.y][r.x + 1] is not None:
            if not themap[r.y][r.x + 1].checkpath(11):  # Adjacent room doesn't have LEFT path
                r.remove_path(7)
                if r.roomright in rooms:
                    print(r.roomright.name)
                    rooms.remove(r.roomleft)



def delete_unreachable_rooms(themap, rooms, start_x=2, start_y=2):
    """
    Remove rooms from `themap` and `rooms` that are not reachable from the
    starting room at (start_x, start_y).

    This does a BFS following valid mutual connections (uses `checkpath`).
    It updates `themap` in-place (sets unreachable entries to None) and
    replaces the contents of `rooms` with only the reachable rooms.

    Returns the list of reachable rooms (same object as `rooms`).
    """
    from collections import deque

    # Validate start coords
    if not (0 <= start_y < len(themap) and 0 <= start_x < len(themap[0])):
        return rooms

    start = themap[start_y][start_x]
    if start is None:
        return rooms

    # Directions: (code, dx, dy, opposite_code)
    directions = [
        (2, 0, -1, 3),   # UP
        (3, 0, 1, 2),    # DOWN
        (7, 1, 0, 11),   # RIGHT
        (11, -1, 0, 7)   # LEFT
    ]

    reachable = set()
    q = deque()
    q.append(start)
    reachable.add((start.x, start.y))

    while q:
        r = q.popleft()
        for code, dx, dy, opp in directions:
            nx, ny = r.x + dx, r.y + dy
            if not r.checkpath(code):
                continue
            if not (0 <= ny < len(themap) and 0 <= nx < len(themap[0])):
                continue
            nbr = themap[ny][nx]
            if nbr is None:
                continue
            # ensure the neighbour also has the reciprocal path
            if not nbr.checkpath(opp):
                continue
            coord = (nbr.x, nbr.y)
            if coord not in reachable:
                reachable.add(coord)
                q.append(nbr)

    # Remove unreachable rooms from the map and from the rooms list
    new_rooms = []
    for r in rooms:
        if (r.x, r.y) in reachable:
            new_rooms.append(r)
        else:
            # clear from map
            if 0 <= r.y < len(themap) and 0 <= r.x < len(themap[0]):
                themap[r.y][r.x] = None

    rooms.clear()
    rooms.extend(new_rooms)
    return rooms
