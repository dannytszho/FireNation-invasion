import pygame

from pygame.sprite import Sprite

class Amon(Sprite):
	"""A class to represent a single amon in the fleet."""

	def __init__(self, ai_game):
		"""Initialize the amon and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings_sky = ai_game.settings_sky

		#Load the amon image and set its rect attribute.
		self.image = pygame.image.load('images/warship.bmp')
		self.rect = self.image.get_rect()

		#Start each new amon near top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#store the amon's exact horizontal position.
		self.x = float(self.rect.x)

	#def auto_move(self, vel):
		#self.rect.y += vel

	def check_edges(self):
		"""Return True if amon is at edge of screen."""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True



	def update(self):
		"""Move the amon right of left."""
		self.x += (self.settings_sky.amon_speed * self.settings_sky.fleet_direction)
		self.rect.x = self.x

