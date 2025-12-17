# Created by Matthew with the help of ChatGPT
# import necessary modules
# core game loop
# input
# update
# draw
'''
GOALS: Kill as many mobs as possible
RULES: use the keys "W", "A","S","D" to move around the map killing the mobs using the bullets by pressing space 
FEEDBACK: health system, make mobs do damage, death screen, gravity, add other levels
FREEDOM: player can move around the map trying to avoid mobs and kill them with bullets before you die going from level to level.

'''

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
      self.game_over = False

      # Cooldown 
      self.shoot_cooldown = Cooldown(400)   # cooldown in ms

      # Added for multi-level support Help from Chatgpt
      self.levels = ["level1.txt", "level2.txt", "level3.txt", "level4.txt"]
      self.current_level_index = 0

   # Added method for level sequence Asked Chat GPT
   def next_level_file(self):
      self.current_level_index += 1
      if self.current_level_index >= len(self.levels):
         self.current_level_index = 0  # wrap around to level 1 if finished all
      return self.levels[self.current_level_index]



# Efficient way to add images
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

      # this is for the tilemap 
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
# Made it so that you press R to restart game
         if self.game_over:
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
               self.game_over = False
               self.new()
            return

         # shooting cooldown
         if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if self.shoot_cooldown.ready():
               self.player.shoot()
               self.shoot_cooldown.start()

         if event.type == pg.MOUSEBUTTONDOWN:
            print("I can get input from mousey mouse mouse mousekerson")

# Spawn random mobs
   def spawn_random_mobs(self, count):
      for _ in range(count):
         while True:
            x = randint(1, 20)
            y = randint(1, 20)
            wall_hit = any(wall.rect.collidepoint(x * TILESIZE[0], y * TILESIZE[1]) for wall in self.all_walls)
            if not wall_hit:
               Mob(self, x, y)
               break

   def load_new_map(self, filename):
       self.map = Map(path.join(self.game_folder, filename))
       self.all_sprites.empty()
       self.all_mobs.empty()
       self.all_walls.empty()
       self.all_coins.empty()
       self.all_projectiles.empty()

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

   def update(self):
      if self.game_over:
         return

      if self.player.health <= 0:
         self.game_over = True
         return

      self.all_sprites.update()
      seconds = pg.time.get_ticks() // 1000
      countdown = 10
      self.time = countdown - seconds

      if len(self.all_mobs) == 0:
         mob_count = randint(2, 4)
         self.spawn_random_mobs(mob_count)

# Draws text
   def draw_text(self, surface, text, size, color, x, y):
      font_name = pg.font.match_font('arial')
      font = pg.font.Font(font_name, size)
      text_surface = font.render(text, True, color)
      text_rect = text_surface.get_rect()
      text_rect.midtop = (x, y)
      surface.blit(text_surface, text_rect)

# Health bar help from Chatgpt
   def draw_health_bar(self, x, y, health):
      max_health = 100
      bar_width = 100
   
      bar_height = 10   
      if health < 0:
          health = 0
      fill = (health / max_health) * bar_width
      outline_rect = pg.Rect(x, y, bar_width, bar_height)
      fill_rect = pg.Rect(x, y, fill, bar_height)
      pg.draw.rect(self.screen, RED, fill_rect)
      pg.draw.rect(self.screen, WHITE, outline_rect, 2)

# Death screen
   def show_death_screen(self):
      self.screen.fill(BLACK)
      self.draw_text(self.screen, "YOU DIED", 64, RED, WIDTH // 2, HEIGHT // 3)
      self.draw_text(self.screen, "Press R to Restart", 32, WHITE, WIDTH // 2, HEIGHT // 2)
      pg.display.flip()

# draws text screen
   def draw(self):
      if self.game_over:
         self.show_death_screen()
         return

      self.screen.fill(BLACK)
      self.all_sprites.draw(self.screen)
      # Draw the smaller health bar above the player
      bar_x = self.player.rect.centerx - 50  # half of new bar_width
      bar_y = self.player.rect.top - 15      # above the player
      self.draw_health_bar(bar_x, bar_y, self.player.health)
      self.draw_text(self.screen, str(self.player.coins), 24, WHITE, 400, 100)
      self.draw_text(self.screen, str(self.time), 24, WHITE, 500, 100)
      pg.display.flip()


if __name__ == "__main__":
   g = Game()
   g.new()
   g.run()
