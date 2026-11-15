import pygame
pygame.init()

screen1 = pygame.display.set_mode((800, 400))
xvel = 0
yvel = 0
yaccel = 0.3
grounded = False

def group_touch(obj, spr_group):
    detect = False
    for x in spr_group:
        if obj.rect.colliderect(x):
            detect = True
            break
    return detect

class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_loc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center = spawn_loc)

    def update(self):
        global xvel
        global yvel
        global grounded

        self.rect.move_ip((xvel, yvel))

        #collision detection

        shifted = False
        if group_touch(player, block_list1):
            self.rect.move_ip((0, -5))
            if not group_touch(player, block_list1) and yvel <= 0:
                print("corner correct UP")
                while not(group_touch(player, block_list1)):
                    self.rect.move_ip((0, 1))
                self.rect.move_ip(0, -1)
                shifted = True
            else:
                self.rect.move_ip((0, 10))
                if not group_touch(player, block_list1) and yvel > 0:
                    print("corner correct DOWN")
                    while not(group_touch(player, block_list1)):
                        self.rect.move_ip((0, -1))
                    self.rect.move_ip(0, 1)
                    shifted = True
                else:
                    self.rect.move_ip((0, -5))

        if group_touch(player, block_list1) and not(shifted):
            if yvel < 0: #moving upwards
                ceiling_collide = False
                wall_collide = False
                self.rect.move_ip(-1 * xvel, 0)
                if group_touch(player, block_list1):
                    ceiling_collide = True
                self.rect.move_ip(xvel, -1 * yvel)
                if group_touch(player, block_list1):
                    wall_collide = True
                self.rect.move_ip(0, yvel)
                if ceiling_collide and wall_collide: 
                    print("ceiling and wall (UP)") #i wanna know what happens
                    self.rect.move_ip(-1 * xvel, -1 * yvel)
                    while not(group_touch(player, block_list1)):
                        self.rect.move_ip((0, -1))
                    self.rect.move_ip(0, 1)
                    yvel = 0
                    if xvel < 0:
                        while not(group_touch(player, block_list1)):
                            self.rect.move_ip((-1, 0))
                        self.rect.move_ip((1, 0))
                    else:
                        while not(group_touch(player, block_list1)):
                            self.rect.move_ip((1, 0))
                        self.rect.move_ip((-1, 0))
                    xvel = 0 
                elif ceiling_collide:
                    print("ceiling only (UP)")
                    while group_touch(player, block_list1):
                        self.rect.move_ip((0, 1))
                    yvel = 0
                elif wall_collide:
                    print("wall only (UP)")
                    if xvel > 0: #moving up+right
                        while group_touch(player, block_list1):
                            self.rect.move_ip((-1, 0))
                    else:
                        while group_touch(player, block_list1):
                            self.rect.move_ip((1, 0))
                    xvel = 0
                if not(ceiling_collide or wall_collide):
                    print("none (UP)")
                    self.rect.move_ip(0, -1 * yvel)
                    while not(group_touch(player, block_list1)): #extreme damger (maybe) this one doesn't upwarp me to the sun so it's probably fine
                        self.rect.move_ip((0, -1))
                    self.rect.move_ip(0, 1)
                    yvel = 0
            elif yvel >= 0: #moving downwards
                floor_collide = False
                wall_collide = False
                self.rect.move_ip(-1 * xvel, 0)
                if group_touch(player, block_list1):
                    floor_collide = True
                self.rect.move_ip(xvel, -1 * yvel)
                if group_touch(player, block_list1):
                    wall_collide = True
                self.rect.move_ip(0, yvel)
                if floor_collide and wall_collide:
                    print("floor and wall (DOWN / NONE)")
                    self.rect.move_ip(-1 * xvel, -1 * yvel)
                    while not(group_touch(player, block_list1)):
                        self.rect.move_ip((0, 1))
                    self.rect.move_ip(0, -1)
                    yvel = 0
                    if xvel < 0:
                        while not(group_touch(player, block_list1)):
                            self.rect.move_ip((-1, 0))
                        self.rect.move_ip((1, 0))
                    else:
                        while not(group_touch(player, block_list1)):
                            self.rect.move_ip((1, 0))
                        self.rect.move_ip((-1, 0))
                    xvel = 0
                elif wall_collide:
                    print("wall only (DOWN / NONE)")
                    if xvel > 0: #moving down+right
                        while group_touch(player, block_list1):
                            self.rect.move_ip((-1, 0))
                    else:
                        while group_touch(player, block_list1):
                            self.rect.move_ip((1, 0))
                    xvel = 0
                elif floor_collide:
                    print("floor only (DOWN / NONE)")
                    while group_touch(player, block_list1):
                        self.rect.move_ip((0, -1))
                    yvel = 0
                if not(floor_collide or wall_collide):
                    print("none (DOWN / NONE)")
                    self.rect.move_ip(0, -1 * yvel)
                    while not(group_touch(player, block_list1)): #extreme damger (maybe)
                        self.rect.move_ip((0, 1))
                    self.rect.move_ip(0, -1)
                    yvel = 0

        self.rect.move_ip(0, 5) #ground detection
        if group_touch(player, block_list1):
            grounded = True
        else:
            grounded = False
        self.rect.move_ip(0, -5)
        
        if inputs[0] and xvel > -5:
            xvel -= 0.6
        if inputs[1] and xvel < 5:
            xvel += 0.6
        if not(inputs[0] or inputs[1]):
            if xvel > 0:
                xvel -= 0.6
                if xvel < 0:
                    xvel = 0
            else:
                xvel += 0.6
                if xvel > 0:
                    xvel = 0
        if inputs[2] and grounded:
            print("jump")
            yvel = -8 #jump
            inputs[2] = False

        if self.rect.centery > 390:
            yvel = -12
            print("bottom bounce")
            

class Block(pygame.sprite.Sprite):
    def __init__(self, width, height, spawn_loc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 150))
        self.rect = self.image.get_rect(center = spawn_loc)

player = Player((400, 100))
block = Block(300, 30, (400, 330))
block2 = Block(100, 30, (600, 325))
block3 = Block(50, 75, (250, 290))
block4 = Block(100, 15, (300, 260))
block5 = Block(30, 300, (650, 180))

sp_list1 = pygame.sprite.Group()
block_list1 = pygame.sprite.Group()

sp_list1.add(player)
block_list1.add(block)
block_list1.add(block2)
block_list1.add(block3)
block_list1.add(block4)
block_list1.add(block5)

game_active = True
inputs = [False, False, False]
while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                inputs[0] = True
            elif event.key == pygame.K_d:
                inputs[1] = True
            elif event.key == pygame.K_w:
                inputs[2] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                inputs[0] = False
            elif event.key == pygame.K_d:
                inputs[1] = False
            elif event.key == pygame.K_w:
                inputs[2] = False

    if grounded:
        screen1.fill((30, 30, 30))
    else:
        screen1.fill((0, 0, 0))
    
    player.update()
    if yvel < 8 and not(grounded):
        yvel += yaccel
    
    sp_list1.draw(screen1)
    block_list1.draw(screen1)
    pygame.display.update()
    pygame.time.Clock().tick(60)