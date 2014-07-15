##############################################################################
# microburst.py                                                              #
# current contributors: Sam Weiss                                            #
#                                                                            #
# This file will contain the main game loop as well as some supporting       #
# functions for the Microburst burst.                                        #
##############################################################################

import pygame, os, sys, random, time
from pygame.locals import *

'''
+----------------------------------------------------------------------------+
|                                                                            |
|                          Game Sprite Definitions                           |
|                                                                            |
+----------------------------------------------------------------------------+
'''
class sprite_base(pygame.sprite.Sprite):
    '''a base class for objects to streamline'''
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except pygame.error, message:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def __init__(self, screen, x, y, dx, dy, img_name):
        '''intit values that are in every sprite'''
        self.image = self.load_image(img_name)
        self.screen = screen
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = self.image.get_rect()
        self.image_w, self.image_h = self.image.get_size()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

    def draw(self):
        '''call the screen draw function'''
        '''angles'''
        self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        '''check to make sure that moving will not move you out of bounds'''
        if self.x + self.dx > 0 and self.x + self.dx < screen.width - self.image_w:
            self.x += self.dx
        if self.y + self.dy > 0 and self.y+self.dy < (screen.height - self.image_h):
            self.y += self.dy
        '''update the rectangle if it does not'''
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

class player(sprite_base):
    '''create a class for the player'''
    def __init__(self, screen, x, y, dx, dy, img_name, size):
        self.size = size
        super(screen, x, y, dx, dy, img_name)
    def update(self, keys):
        for i in keys:
            if i == "UP":
                self.dy = - 3
            if i == "DOWN":
                self.dy = 3
            if i == "LEFT":
                self.dx = - 3
            if i == "RIGHT":
                self.dx = 3
        super.update()

class enemy(sprite_base):
    def __init__(self, screen, x, y, dx, dy, img_name, size):
        self.size = size
        super(screen, x, y, dx, dy, img_name)

    def update(self):
        if self.x + self.dx < 0 or self.x+self.dy > (screen.width - self.image_w): 
            self.dx = -1 * self.dx;
        if self.y + self.dy > 0 and self.y+self.dy < (screen.width - self.image_h):
            self.dy = -1 * self.dy
        super.update()

class food(sprite_base):
    def __init__(self, screen, x, y, dx, dy, img_name, size):
        self.size = size
        super(screen, x, y, dx, dy, img_name)
    '''needswork'''
        

'''
+----------------------------------------------------------------------------+
|                                                                            |
|                           Init function code                               |
|                                                                            |
+----------------------------------------------------------------------------+
'''

def init_game(objects, screen, num_enemies, num_food):
    players = []
    enemies = []
    food = []
    background = []
    players.append(player(screen, 400, 300, 0, 0, "player.png"))
    for i in range(num_enemies):
        enemies.append( enemy(screen, 100, 100, 1, 1, "enemy.png"))
    for i in range(num_food):
        food.append(food( screen, 500, 500, 0, 0, "food.png"))
    background.append(background(screen))
    objects.append(players)
    objects.append(enemies)
    objects.append(food)
    objects.append(background)


'''
+----------------------------------------------------------------------------+
|                                                                            |
|                          Main Execution code                               |
|                                                                            |
+----------------------------------------------------------------------------+
'''
def quit():
    '''quits the game if the game quit signal is provided'''
    pygame.quit()
    sys.exit(0)

#setup pygame and the window

pygame.init
screenDimensions = (800, 600)
window = pygame.display.set_mode(screenDimensions, pygame.RESIZABLE)
pygame.display.set_caption('Microbust')
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
pressed = []
clock = pygame.time.Clock()
'''limit framerate to 60 FPS'''
FPS = 60
'''game length in seconds'''
gamelength = 20
pygame.time.set_timer(USEREVENT + 1, 1000)
'''keep track of the opjects'''
objects = []
'''keep track of what screen we're on'''
screen = 1
gamestart = 0
while True:
    clock.tick(FPS)
    if screen == 1:
        '''draw some intro screen'''
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quit()
                if event.key == K_SPACE:
                    screen = 2
                    gamestart = time.clock()
                    print str(gamestart) + " " +  str(time.clock())
                    init_gameOA(objects, screen)
    elif screen == 3:
        quit()
    elif screen == 2:
        for o in objects[1]:
            if pygame.sprite.collide_rect(objects[0][0],o):
                if objects[0][0].size > o.size:
                    objects[1].remove(o)
                    objects[0][0].size += o.size / 5
                else:
                    screen = 3
        for o in objects[2]:
            if pygame.sprite.collide_rect(objects[0][0],o):
                if objects[0][0].size > o.size:
                    objects[1].remove(o)
                    objects[0][0].size += o.size / 10
                else:
                    o.dx = objects[0][0].dx * 2
                    o.dy = objects[0][0].dy * 2
        for l in objects:
            for o in l:
                l.draw()
                l.update()
        pygame.display.flip()
        if(time.clock() - gamestart >= gamelength):
            screen == 3
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                elif event.key == K_UP:
                    pressed.append("UP")
                elif event.key == K_DOWN:
                    pressed.append("DOWN")
                elif event.key == K_LEFT:
                    pressed.append("LEFT")
                elif event.key == K_RIGHT:
                    pressed.append("RIGHT")
                elif event.key == K_SPACE:
                    pressed.append("SPACE")
            elif event.type == KEYUP:
                if event.key == K_UP:
                    pressed.remove("UP")
                elif event.key == K_DOWN:
                    pressed.remove("DOWN")
                elif event.key == K_LEFT:
                    pressed.remove("LEFT")
                elif event.key == K_RIGHT:
                    pressed.remove("RIGHT")
                elif event.key == K_SPACE:
                    pressed.remove("SPACE")
