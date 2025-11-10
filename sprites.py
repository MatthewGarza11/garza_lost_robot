# File created by: Chris Cozort

# The sprites module contains all the sprites
# Sprites include: player, mob - moving object

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import Cooldown
from random import randint
from random import choice
vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(game.player_img, (128, 128))
        self.image = game.player_img
        self.image.set_colorkey(BLACK)
        self.image_img = game.player_img
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.speed = 250
        self.health = 100
        self.coins = 0
        self.cd = Cooldown(1000)
        self.dir = vec(0, -1)  # default facing up

    def get_keys(self):
        self.vel = vec(0, Gravity)
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            # make sure player has a direction
            if self.dir.length_squared() == 0:
                self.dir = vec(0, -1)  # default shoot up
            # create projectile
            Projectile(self.game, self.rect.centerx, self.rect.centery, self.dir)
        if keys[pg.K_w]:
            self.vel.y = -self.speed*self.game.dt
            self.dir = vec(0,-1)
        if keys[pg.K_a]:
            self.vel.x = -self.speed*self.game.dt
            self.dir = vec(-1,0)
        if keys[pg.K_s]:
            self.vel.y = self.speed*self.game.dt
            self.dir = vec(0,1)
        if keys[pg.K_d]:
            self.vel.x = self.speed*self.game.dt
            self.dir = vec(1,0)
        if self.vel[0] != 0 and self.vel[1] != 0:
            self.vel *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.left - self.rect.width
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.x += self.vel.x
                    else:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.top - self.rect.height
                    else:
                        self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmovable":
                                self.pos.y = hits[1].rect.bottom
                    else:
                        self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            if str(hits[0].__class__.__name__) == "Mob":
                if self.cd.ready():
                    self.health -= 10
                    self.cd.start()
            if str(hits[0].__class__.__name__) == "Coin":
                self.coins += 1
                print(self.coins)

    def update(self):
        self.get_keys()
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_coins, True)
        if not self.cd.ready():
            self.image = self.game.player_img
            print("not ready")
        else:
            self.image = self.game.player_img
            print("ready")

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(choice([-1,1]), choice([-1,1]))
        self.pos = vec(x,y)*TILESIZE[0]
        self.speed = 5
        self.health = 100  # Added this line so mobs can take damage
        print(self.pos)
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.rect.x = self.pos.x
                self.vel.x *= choice([-1,1])
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.rect.y = self.pos.y
                self.vel.y *= choice([-1,1])
    def update(self):
        if self.game.player.pos.x > self.pos.x:
            self.vel.x = 1
        else:
            self.vel.x = -1
        if self.game.player.pos.y > self.pos.y:
            self.vel.y = 1
        else:
            self.vel.y = -1
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = game.coin_img
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
        pass

class Wall(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.state = state
        

        # choose image based on state
        if self.state == "moveable":
            self.image = game.moveable_wall_img
        else:
            self.image = game.wall_img

        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    print("a wall collided with a wall")
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].pos.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.left - self.rect.width
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].pos.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.right
                    else:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    print('wall y collide down')
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].pos.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.top - self.rect.height
                    else:
                        self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].pos.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmovable":
                                self.pos.y = hits[1].rect.bottom
                    else:
                        self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')



class Projectile(Sprite):
    def __init__(self, game, x, y, dir):
        self.game = game
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((16, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = dir.normalize()  # <-- ensures consistent speed
        self.pos = vec(x, y)
        self.rect.center = (x, y)
        self.speed = 10
        self.damage = 25

    def update(self):
        # Move bullet
        self.pos += self.vel * self.speed
        self.rect.center = self.pos

        # Check collision with walls
        if pg.sprite.spritecollideany(self, self.game.all_walls):
            self.kill()

        # Check collision with mobs
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        if hits:
            for mob in hits:
                mob.health -= self.damage
                print(f"Mob hit! Health: {mob.health}")
                if mob.health <= 0:
                    mob.kill()
            self.kill()