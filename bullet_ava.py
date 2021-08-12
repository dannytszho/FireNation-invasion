import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class to manage bullets fired from ava."""
	def __init__(self, ai_game):
		"""Create a bullet object at the ship's current position."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings_sky = ai_game.settings_sky
		self.color = self.settings_sky.bullet_color

		"""Create a bullet rect at (0, 0) and then set correct position."""
		self.rect = pygame.Rect(0, 0, self.settings_sky.bullet_width, self.settings_sky.bullet_height)
		self.rect.midtop = ai_game.ava.rect.midtop

		#Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)

	def update(self):
		"""Move the bullet up the screen."""
		#Update the decimal position of the bullet.
		self.y -= self.settings_sky.bullet_speed
		#Update the rect position.
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw the bullet to the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect)