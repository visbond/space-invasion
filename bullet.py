import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class to manage bullets fired from the ship"""
	def __init__(self, ai_game):
		"""Create a bullet object at the ship's current position."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color
		# Create a bullet rect at (0, 0) and then set correct position.
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
		self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop
		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)
		pass
	#end init def
	
	def update(self):
		"""Move the bullet up the screen."""
		# Update the decimal position of the bullet.
		self.y -= self.settings.bullet_speed	#recall from the ship speed discussion, that this is a float, so being modified first and then its integer part being assigned to int rect.x below
		# Update the rect position.
		self.rect.y = self.y
		#note that there is no x-axis since, once-fired, bullet only moves upward; doesn't move with the ship
		pass
	#end def

	def draw_bullet(self):
		"""Draw the bullet to the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect) #note we are using pygame.draw() rather than display(), since are drawing a rectangle from the coordinates, not displaying a pre-cooked image/surface
		pass
	#end def

	pass
#end class def