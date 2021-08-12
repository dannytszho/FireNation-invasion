import pygame
from pygame.sprite import Sprite

class Ava(Sprite):

	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings_sky = ai_game.settings_sky
		self.screen_rect = ai_game.screen.get_rect()

		self.image = pygame.image.load('images/ava.bmp')
		self.rect = self.image.get_rect()
		self.rect.bottomright = self.screen_rect.bottomright

		#Store a decimal value for the ava's position
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		#Movement flags
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self):
		"""Update avatar's position based on movement flag"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings_sky.ava_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings_sky.ava_speed
		if self.moving_up and self.rect.top > 0:
			self.y -= self.settings_sky.ava_speed
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.y += self.settings_sky.ava_speed

		#Update rect object from self.x and self.y
		self.rect.x = self.x
		self.rect.y = self.y

	def blitme(self):
		self.screen.blit(self.image, self.rect)

	def center_ava(self):
		"""Center the ava on the screen."""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)