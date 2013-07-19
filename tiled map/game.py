from __future__ import print_function, division
import pygame
from pygame.locals import *
from map_tiled import Map

class Game():
	""" main logic.
	
	properties:
		map:	map.Map()

	"""
	done = False
	
	def __init__(self, width=640, height=480):
		pygame.init()
		self.width, self.height = width, height
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((self.width, self.height))

		pygame.display.set_caption("demo: tiled map")

		self.map = Map()

	def main_loop(self):
		# main loop
		while not self.done:
			self.handle_events()
			self.draw()
			self.clock.tick()

	def handle_events(self):
		# handle and copy events if needed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True

			# keydown
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.done = True
				elif event.key == K_s:
					self.map_scrolling = not self.map_scrolling
				elif event.key == K_SPACE:
					self.map.randomize()

			elif event.type == MOUSEMOTION:
				self.map.scroll(event.rel)

	def draw(self):
		# render
		self.screen.fill(Color("gray20"))
		#self.map.draw()
		pygame.display.flip()


if __name__ == "__main__":
	game = Game()
	game.main_loop()