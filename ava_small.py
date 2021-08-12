import pygame
from pygame.sprite import Sprite

class Ava(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings_sky = ai_game.settings_sky
        self.screen_rect = ai_game.screen.get_rect()
        
        self.image = pygame.image.load('images/ava_small.bmp')
        self.rect = self.image.get_rect()
        self.rect.bottomright = self.screen_rect.bottomright
        
        #Store a decimal value for the ava's position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ava(self):
        """Center the ava on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)