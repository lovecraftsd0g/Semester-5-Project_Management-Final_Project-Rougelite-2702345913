import random
from Entities.Player import Player_Character
from Entities.Player import Atk
from Entities.enemy import zombie
from Entities.entity import portal
from roomStuff.Method_Hub import generate_rooms
from roomStuff.Method_Hub import generateContents
from roomStuff.Method_Hub import generate_current_room_tiles as generate_room_tiles
from roomStuff.Method_Hub import remove_improper_paths
from roomStuff.Method_Hub import run_game as run_game
from roomStuff.room_stuff import roomv2 as room
from roomStuff.tiles import tile as t
import pygame

pygame.init()
Player_resources = 0
room_Score = 0
scx = 320
scy = 320
window = pygame.display.set_mode((scx,scy))

clock = pygame.time.Clock()

tiles = pygame.sprite.Group()

player = Player_Character((scx/2,scy/2), tiles)

#map of multitude of rooms
        #    0     1     2     3     4
the_map = [[None, None, None, None, None], # 0 
           [None, None, None, None, None], # 1
           [None, None, None, None, None], # 2
           [None, None, None, None, None], # 3
           [None, None, None, None, None]] # 4
            #0  1  2  3  4  5  6  7  8  9#
the_room = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Top wall
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # Left and right walls
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # Bottom wall

room_list = []

generate_rooms(the_map, room_list)

playergridx = 2
playergridy = 2
prev_gridx, prev_gridy = playergridx, playergridy


#door positions in tile index form, to open the door loop through the tile group and remove the tile with those indexes
#using index_X and index_Y from tiles.py


for y in range(len(the_room)):
    for x in range(len(the_room[y])):
        if the_room[y][x] != 1:
            continue
        # By default place the wall tile
        tiles.add(t("Images/tiles/test_01.png", (x * 32 + 16, y * 32 + 16), True))


for row in the_map:
        print([str(room) if room is not None else "None" for room in row])

#close it, but also determine entering gets resources, or into a fight
                    

#remove_improper_paths(the_map, room_list)

generate_room_tiles(tiles, the_map, playergridx, playergridy)
#entities and monsters
EnemyGroup = the_map[playergridy][playergridx].EneGroup
atk = Atk((player.rect.centerx, player.rect.centery), EnemyGroup, (200,200))
pAtkGroup = pygame.sprite.Group()
players = pygame.sprite.Group()
players.add(player)
pAtkGroup.add(atk)

portalGroup = pygame.sprite.Group()  # Create portal group


current_Screen_value = 1
# Print more readable room list

room_len = len(room_list) - 1
rand_pick = random.randint(0, room_len)
room_list[rand_pick].exit = True

portal1 = portal((scx//2, scy//2))
for Room in room_list:
    Room.Rconnect(the_map)
soruce_room = the_map[2][2]
portalGroup.add(portal1)  # Add portal to portal group

#the running
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if current_room.name == "TBLR" and Player_resources >= 2 and room_Score < 5:
                            #     1     2    3      4     5
                    the_map = [ [None, None, None, None, None], # 0 
                                [None, None, None, None, None], # 1
                                [None, None, None, None, None], # 2
                                [None, None, None, None, None], # 3
                                [None, None, None, None, None]] # 4
                    room_list = []
                    generate_rooms(the_map, room_list)
                    #remove_improper_paths(the_map, room_list)
                    for Room in room_list:
                        Room.Rconnect(the_map)
                    generate_room_tiles(tiles, the_map, playergridx, playergridy)
                    soruce_room = the_map[2][2]
                    soruce_room.quantity = 0
                    soruce_room.entered = True
                    soruce_room.lootOrMonster = False
                    soruce_room.interacted = True
                    playergridx = 2
                    playergridy = 2

                    print("Regenerated map due to lack of resources")
                    for row in the_map:
                        print([str(room) if room is not None else "None" for room in row])
                    Player_resources = 0
                    room_Score += 1
    
    #print(playergridx, playergridy)
    current_room = the_map[playergridy][playergridx]

    hits = pygame.sprite.spritecollide(player, EnemyGroup, False)  # False = don't remove enemies
    # Handle damage to player
    for hit in hits:
        player.knife -= 1
        print("Player knife count:", player.knife)
        hit.kill()  # Remove the enemy that hit the player

    if not portal1 in soruce_room.EntGrp:
        soruce_room.EntGrp.add(portal1)

    #handle moving off screen and changing room grid
    if player.rect.centerx > scx:
        if EnemyGroup.sprites() == []:
            player.rect.centerx = 0
            playergridx += 1
        elif EnemyGroup.sprites() != []:
            player.rect.centerx = scx - 40

    if player.rect.centerx < 0:
        if EnemyGroup.sprites() == []:
            player.rect.centerx = scx
            playergridx -= 1
        elif EnemyGroup.sprites() != []:
            player.rect.centerx = 40

    if player.rect.centery > scy:
        if EnemyGroup.sprites() == []:
            player.rect.centery = 0
            playergridy += 1
        elif EnemyGroup.sprites() != []:
            player.rect.centery = scy - 40

    if player.rect.centery < 0:
        if EnemyGroup.sprites() == []:
            player.rect.centery = scy
            playergridy -= 1
        elif EnemyGroup.sprites() != []:
            player.rect.centery = 40


    # if we moved to a different room grid, regenerate the tiles for the new room
    if (playergridx, playergridy) != (prev_gridx, prev_gridy):
        # clamp to map bounds to avoid index errors
        prev_gridx, prev_gridy = playergridx, playergridy
        generate_room_tiles(tiles, the_map, playergridx, playergridy)
        EnemyGroup = the_map[playergridy][playergridx].EneGroup
        atk.enemy_group = EnemyGroup
        if current_room is not None and current_room.name != "TBLR" and current_room.entered == False:
            if current_room.entered == False and current_room.lootOrMonster == True:
                current_room.group = EnemyGroup
                Player_resources += 1
                print("Player resources:", Player_resources)
                # FIX → mark before spawning
                current_room.entered = True
                current_room.interacted = True 
                
                generateContents(current_room, player)
            current_room = the_map[playergridy][playergridx]
            if current_room.entered == False:
                Player_resources += current_room.quantity
                current_room.entered = True
                current_room.interacted = True
                print("Player resources:", Player_resources)

    # Enemy movement towards player
    # for enemy in EnemyGroup:
    #     enemy.move_towards_player()

    # Drawing and game logic based on current screen
    if current_Screen_value == 1:
        run_game(player, tiles, clock, window, EnemyGroup, players, pAtkGroup, atk, Player_resources, current_room.EntGrp, room_Score)

        if player.knife <=0 or Player_resources < 0:
            EnemyGroup.empty()
            players.empty()
            pAtkGroup.empty()
            window.fill((0,0,0))
            print("Game Over")
            current_Screen_value = 2
        elif room_Score >= 5:
            EnemyGroup.empty()
            players.empty()
            pAtkGroup.empty()
            window.fill((0,0,0))
            print("You Win!")
            current_Screen_value = 3
    elif current_Screen_value == 2:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Game Over!", True, (255, 0, 0))
        window.blit(text, (scx//2 - 60, scy//2 - 25))
        #button to reset
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            #reset game
            EnemyGroup.empty()
            players.empty()
            pAtkGroup.empty()
            player = Player_Character((scx/2,scy/2), tiles)
            players.add(player)
            atk = Atk((player.rect.centerx, player.rect.centery), EnemyGroup, (200,200))
            pAtkGroup.add(atk)
            Player_resources = 0
            room_Score = 0
            playergridx = 2
            playergridy = 2
            prev_gridx, prev_gridy = playergridx, playergridy
            the_map = [ [None, None, None, None, None], # 0 
                        [None, None, None, None, None], # 1
                        [None, None, None, None, None], # 2
                        [None, None, None, None, None], # 3
                        [None, None, None, None, None]] # 4
            room_list = []
            generate_rooms(the_map, room_list)
            #remove_improper_paths(the_map, room_list)           
            for Room in room_list:
                Room.Rconnect(the_map)
            generate_room_tiles(tiles, the_map, playergridx, playergridy)
            soruce_room = the_map[2][2]
            soruce_room.quantity = 0
            soruce_room.entered = True
            soruce_room.lootOrMonster = False
            soruce_room.interacted = True
            current_Screen_value = 1
        pygame.display.flip()
    elif current_Screen_value == 3:
        font = pygame.font.SysFont(None, 55)
        text = font.render("You Win!", True, (0, 255, 0))
        window.blit(text, (scx//2 - 60, scy//2 - 25))

        #button to reset
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            #reset game
            EnemyGroup.empty()
            players.empty()
            pAtkGroup.empty()
            player = Player_Character((scx/2,scy/2), tiles)
            players.add(player)
            atk = Atk((player.rect.centerx, player.rect.centery), EnemyGroup, (200,200))
            pAtkGroup.add(atk)
            Player_resources = 0
            room_Score = 0
            playergridx = 2
            playergridy = 2
            prev_gridx, prev_gridy = playergridx, playergridy
            the_map = [ [None, None, None, None, None], # 0 
                        [None, None, None, None, None], # 1
                        [None, None, None, None, None], # 2
                        [None, None, None, None, None], # 3
                        [None, None, None, None]] # 4
            room_list = []
            generate_rooms(the_map, room_list)
            #remove_improper_paths(the_map, room_list)
            for Room in room_list:
                Room.Rconnect(the_map)
            generate_room_tiles(tiles, the_map, playergridx, playergridy)
            print(f'rooms: {room_list}')
            soruce_room = the_map[2][2]
            soruce_room.quantity = 0
            soruce_room.entered = True
            soruce_room.lootOrMonster = False
            soruce_room.interacted = True
            current_Screen_value = 1
        
        
        pygame.display.flip()



