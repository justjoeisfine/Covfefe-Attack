
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):
		"""Intitialize the ship at start position."""
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# Load the ship image and get its rect.
		self.image = pygame.image.load('images/rocketCUT3.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		# Start new ship at bottom of screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		# Store a decimal value for ship's centerpoint
		self.center = float(self.rect.centerx)
		
		# Movement flags
		self.moving_right = False
		self.moving_left = False
		
	def update(self):
		""" Update ship position based on movement flag """
		# Update the shp's center value, not the rect
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
			
		# Update rect object from self.center
		self.rect.centerx = self.center
						
	def blitme(self):
		"""Draw the ship at current location."""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Center the ship on the screen"""
		self.center = self.screen_rect.centerx
		
