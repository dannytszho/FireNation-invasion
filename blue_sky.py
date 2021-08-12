import sys
from time import sleep

import pygame

from settings_sky import Settings
from game_stats_sky import GameStats
from scoreboard import Scoreboard
from button import Button
from ava import Ava
from bullet_ava import Bullet
from amon import Amon


class Game:
	"""Over class to manage game assets and behavior."""
	def __init__(self):
		pygame.init()

		self.settings_sky = Settings()
		self.screen = pygame.display.set_mode((self.settings_sky.screen_width, self.settings_sky.screen_height))
		pygame.display.set_caption('Avatar Invasion')

		#Create an instance to store game statistics,
		# and create a scoreboard.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ava = Ava(self)
		self.bullets = pygame.sprite.Group()
		self.amons = pygame.sprite.Group()

		self._create_fleet()

		#Make the Play button.
		self.play_button = Button(self, "Let's Play!")


	def run_game(self):
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ava.update()
				self._update_bullets()
				self._update_amons()
			self._update_screen()


	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks play."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#Reset the game settings.
			self.settings_sky.initialize_dynamic_settings()
			#Reset the game statistics.
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level( )
			self.sb.prep_avas()

			#Get rid of any remaining amons and bullets.
			self.amons.empty()
			self.bullets.empty()

			#Create a new fleet and center the ava.
			self._create_fleet()
			self.ava.center_ava()

			#Hide the mouse cursoe.
			pygame.mouse.set_visible(False)


	def _check_keydown_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ava.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ava.moving_left = True
		elif event.key == pygame.K_UP:
			self.ava.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.ava.moving_down = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()


	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ava.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ava.moving_left = False
		elif event.key == pygame.K_UP:
			self.ava.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.ava.moving_down = False

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets) < self.settings_sky.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update bullet positions."""
		self.bullets.update()
		#Make sure bullets on store in a copy list, and get rid of the bullets thar have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		#Check for any bullets that have hit amons.
		#If so, get rid of the bullet and amon.
		self._check_bullet_amon_collisions()

	def _check_bullet_amon_collisions(self):
		collisions = pygame.sprite.groupcollide(self.bullets, self.amons, True, True)
		if not self.amons:
			#Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			self.settings_sky.increase_speed()

			#Increase level
			self.stats.level += 1
			self.sb.prep_score()

		if collisions:
			for amons in collisions.values():
				self.stats.score += self.settings_sky.amon_points * len(amons)
			self.sb.prep_score()
			self.sb.check_high_score()


	def _create_fleet(self):
		"""Create a fleet of amons."""
		#Make an amon.
		amon = Amon(self)
		amon_width = amon.rect.width
		amon_width, amon_height = amon.rect.size
		available_space_x = self.settings_sky.screen_width #- (2* amon_width)
		number_amon_x = available_space_x // (2* amon_width)
		
		ava_height = self.ava.rect.height
		available_space_y = self.settings_sky.screen_height - (6*amon_height)- ava_height
		number_rows = available_space_y // (2*amon_height)
		#Create the full fleet of aliens.
		for row_number in range(number_rows):
			for amon_number in range(number_amon_x):
				self._create_amon(amon_number, row_number)
			#Create an alien and place it in the row.

	def _create_amon(self, amon_number, row_number):
		amon = Amon(self)
		amon_width, amon_height = amon.rect.size
		amon.x = amon_width + 2 * amon_width * amon_number
		amon.rect.x = amon.x
		amon.rect.y = amon.rect.height + 2 * amon.rect.height *row_number
		self.amons.add(amon)

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge."""
		for amon in self.amons.sprites():
			if amon.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		for amon in self.amons.sprites():
			amon.rect.y += self.settings_sky.fleet_drop_speed
		self.settings_sky.fleet_direction *= -1	

	def _ava_hit(self):
		"""Respond to the ava being hit by an ava."""
		if self.stats.avas_left > 0:
			#Decrement avas_left, and update scoreboard.
			self.stats.avas_left -= 1
			self.sb.prep_avas()

			#Get rid of any remaining amons and bullets.
			self.amons.empty()
			self.bullets.empty()

			#Create a new fleet and center the ava.
			self._create_fleet()
			self.ava.center_ava()

			#Pause.
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_amons_bottom(self):
		"""Check if any amons have reached the bottom of the screen."""
		screen_rect = self.screen.get_rect()
		for amon in self.amons.sprites():
			if amon.rect.bottom >= screen_rect.bottom:
				#Treat this the same as if the ava got hit
				self._ava_hit()
				break

	def _update_amons(self):
		self._check_fleet_edges()
		self.amons.update()

		#Look for amon-ava collisions.
		if pygame.sprite.spritecollideany(self.ava, self.amons):
			self._ava_hit()

		#Look for amons hitting the bottom of the screen.
		self._check_amons_bottom()

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings_sky.bg_color)
		self.ava.blitme()

		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.amons.draw(self.screen)

		#Draw the score information.
		self.sb.show_score()

		#Draw the play button if the game is inactive.
		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()

if __name__ == '__main__':

	ai = Game()
	ai.run_game()
