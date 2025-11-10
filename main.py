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
   
   # sets up a game folder directory path using the current folder containing THIS file
   # give the Game class a map property which uses the Map class to parse the level1.txt file
   # loads image files from images folder
   # Used chat for help so i can resize better
   def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.img_folder = path.join(self.game_folder, 'images')
      self.map = Map(path.join(self.game_folder, 'level1.txt'))

      # Load and SCALE your player image
      self.player_img = pg.image.load(path.join(self.img_folder, 'green shooter.png')).convert_alpha()
      self.player_img = pg.transform.scale(self.player_img, (48, 48))  # Resize player

      # Load and SCALE coin image
      self.coin_img = pg.image.load(path.join(self.img_folder, 'Coin.png')).convert_alpha()
      self.coin_img = pg.transform.scale(self.coin_img, (32, 32))  # Resize coin

      # Load and SCALE wall images
      self.wall_img = pg.image.load(path.join(self.img_folder, 'dirty brick 3.png')).convert_alpha()
      self.wall_img = pg.transform.scale(self.wall_img, (32, 32))  # Regular wall size

      self.moveable_wall_img = pg.image.load(path.join(self.img_folder, 'brick (2).png')).convert_alpha()
      self.moveable_wall_img = pg.transform.scale(self.moveable_wall_img, (32, 32))  # Moveable wall size

   def new(self):
      # Create all sprite groups
      self.load_data()
      self.all_sprites = pg.sprite.Group()
      self.all_mobs = pg.sprite.Group()
      self.all_coins = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()
      self.all_projectiles = pg.sprite.Group()
      
      # Create game objects based on map layout
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
         # input
         self.events()
         # process
         self.update()
         # output
         self.draw()
      pg.quit()

   def events(self):
      for event in pg.event.get():
         if event.type == pg.QUIT:
            self.playing = False
         if event.type == pg.MOUSEBUTTONDOWN:
            print("I can get input from mousey mouse mouse mousekerson")

   def update(self):
      self.all_sprites.update()
      seconds = pg.time.get_ticks() // 1000
      countdown = 10
      self.time = countdown - seconds

      if len(self.all_coins) == 0:
         for i in range(2, 5):
            Coin(self, randint(1, 20), randint(1, 20))
         print("I'm BROKE!")

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
