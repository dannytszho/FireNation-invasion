class Settings:

	def __init__(self):
		"""Initialize the game's static settings."""
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (255,255,255)

		#Ava settings
		self.ava_limit = 3

		#Bullet settings
		self.bullet_width = 10
		self.bullet_height = 20
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3
		
		#Amon settings
		self.fleet_drop_speed = 10

		#How quickly the game speedds up
		self.speedup_scale = 1.5

		#How quickly the amon point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game."""
		self.ava_speed = 1.5
		self.bullet_speed = 3.0
		self.amon_speed = 1.0

		#fleet_direction of 1 represents right, -1 represents left.
		self.fleet_direction = 1

		#Scoring
		self.amon_points = 50


	def increase_speed(self):
		"""Increase speed settings and amon point values."""
		self.ava_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.amon_speed *= self.speedup_scale

		self.amon_points = int(self.amon_points * self.score_scale)
		print(self.amon_points)