import os
from random import randint

import pygame
from pygame.locals import *
import numpy as np

TILE_W, TILE_H = 32, 32
named_tile = {"grass":0, "darkgrass":1, "dirt":2, "road":3}

debug = True

class Map():
	"""Stores map info as a 2d numpy array, and renders tiles.
	Map is an array of ints, which correspond to the tile id

	members:
		scrolling:	toggle mouse smooth scrolling of map
		offset:	topleft for scrolling and world<->screen coordinate conversion.
	"""

	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.scrolling = False
		self.load_tileset( os.path.join("art","tileset.bmp"))

		self.reset()
		self.randomize()

	def reset(self, tiles_x=60, tiles_y=40):
		# clear map, and reset to defaults.
		"""
		default to fit for one screen size:
        self.tiles_x = self.game.width / TILE_W
        self.tiles_y = self.game.height / TILE_H
        """
        # or a fixed number
        #self.tiles_x =10
        #tiles_y = 10
        self.tiles_x, self.tiles_y = tiles_x, tiles_y

        # create empty array , filled with zero
        self.tiles = np.zeros((self.tiles_x, self.tiles_y), dtype=int)
        if debug:
        	print("Map().reset(size={}, {})".format(tiles_x, tiles_y))


	def randomize(self):
		# give all tiles random values
		self.offset = (-200, -200)

		# completely random
		for y in range(self.tiles_y):
			for x in range(self.tiles_x):
				self.tiles[x,y] = randint(0, len(named_tile.keys()))

		# example of slicing, to add roads
		self.tiles[1:] = named_tile["road"]
		self.tiles[:2] = named_tile["road"]

		if debug: print("tiles = ", self.tiles)

	def scroll(self, rel):
		#scroll map using relative coordinates
		if not self.scrolling: return

		self.offset = (
				self.offset[0] + rel[0],
				self.offset[1] + rel[1] )

	def load_tileset(self, image="tileset.bmp"):
		# load image
		self.tileset = pygame.image.load(image)
		self.rect = self.tileset.get_rect()

	def draw(self):
		# no optimization, just iterate to render tiles
		# You could start iterating at actual tiles on screen, instead.
		for y in range(self.tiles_y):
			for x in range(self.tiles_x):				
				cur = self.tiles[x][y]
				dest = Rect(x * TILE_W, y * TILE_H, TILE_W, TILE_H)
				src = RECT(cur * TILE_W, 0, TILE_W, TILE_H)

				# screen to world coord
				if self.scrolling:
					dest.left += self.offset[0]
					dest.top += self.offset[1]

				self.screen.blit(self.tileset, dest, src)




