# Created by Matthew with the help of ChatGPT
# import necessary modules
# core game loop
# input
# update
# draw

import math
import random
import sys
import pygame as pg
from settings import *
from sprites import *
from os import path
from utils import *
from math import floor

# overview - CONCISE AND INFORMATIVE
class Game:
   def __init__(self):
      pg.init()
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("Garza's awesome game!!!!!")
      self.playing = True

   # Cooldown 
      self.shoot_cooldown = Cooldown(400)   # cooldown in ms


   def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.img_folder = path.join(self.game_folder, 'images')
      self.map = Map(path.join(self.game_folder, 'level1.txt'))

      self.player_img = pg.image.load(path.join(self.img_folder, 'green shooter.png')).convert_alpha()
      self.player_img = pg.transform.scale(self.player_img, (48, 48))

      self.coin_img = pg.image.load(path.join(self.img_folder, 'Coin.png')).convert_alpha()
      self.coin_img = pg.transform.scale(self.coin_img, (32, 32))

      self.wall_img = pg.image.load(path.join(self.img_folder, 'dirty brick 3.png')).convert_alpha()
      self.wall_img = pg.transform.scale(self.wall_img, (32, 32))

      self.moveable_wall_img = pg.image.load(path.join(self.img_folder, 'brick (2).png')).convert_alpha()
      self.moveable_wall_img = pg.transform.scale(self.moveable_wall_img, (32, 32))

      self.mob_img = pg.image.load(path.join(self.img_folder, 'Angry Alien.png')).convert_alpha()



   def new(self):
      self.load_data()
      self.all_sprites = pg.sprite.Group()
      self.all_mobs = pg.sprite.Group()
      self.all_coins = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()
      self.all_projectiles = pg.sprite.Group()
      
      for row, tiles in enumerate(self.map.data):
         for col, tile in enumerate(tiles):
            if tile == '1':
               Wall(self, col, row, "unmoveable")
            elif tile == '2':
               Wall(self, col, row, "moveable")
            elif tile == 'C':
               Coin(self, col, row)
            elif tile == 'P':
               self.player = Player(self, col, row)
            elif tile == 'M':
               Mob(self, col, row)
     

   def run(self):
      while self.playing:
         self.dt = self.clock.tick(FPS) / 1000
         self.events()
         self.update()
         self.draw()
      pg.quit()


   def events(self):
      for event in pg.event.get():
         if event.type == pg.QUIT:
            self.playing = False

         # added shooting cooldown
         if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if self.shoot_cooldown.ready():
               self.player.shoot()      # call your player's shoot function
               self.shoot_cooldown.start()   # start cooldown timer

         if event.type == pg.MOUSEBUTTONDOWN:
            print("I can get input from mousey mouse mouse mousekerson")


   def spawn_random_mobs(self, count):
      for _ in range(count):
         while True:
            x = randint(1, 20)
            y = randint(1, 20)
            wall_hit = any(wall.rect.collidepoint(x * TILESIZE[0], y * TILESIZE[1]) for wall in self.all_walls)
            if not wall_hit:
               Mob(self, x, y)
               break


   def update(self):
      self.all_sprites.update()
      seconds = pg.time.get_ticks() // 1000
      countdown = 10
      self.time = countdown - seconds

      if len(self.all_mobs) == 0:
         mob_count = randint(2, 4)
         self.spawn_random_mobs(mob_count)
         print(f"All mobs defeated! Respawning {mob_count} new mobs...")


   def draw_text(self, surface, text, size, color, x, y):
      font_name = pg.font.match_font('arial')
      font = pg.font.Font(font_name, size)
      text_surface = font.render(text, True, color)
      text_rect = text_surface.get_rect()
      text_rect.midtop = (x, y)
      surface.blit(text_surface, text_rect)


   def draw(self):
      self.screen.fill(BLACK)
      self.draw_text(self.screen, str(self.player.health), 24, WHITE, 100, 100)
      self.draw_text(self.screen, str(self.player.coins), 24, WHITE, 400, 100)
      self.draw_text(self.screen, str(self.time), 24, WHITE, 500, 100)
      self.all_sprites.draw(self.screen)
      pg.display.flip()


if __name__ == "__main__":
   g = Game()
   g.new()
   g.run()
