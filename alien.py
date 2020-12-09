import pygame
from pygame.sprite import Sprite

class Alien (Sprite):
	'''a class to represent an alien in the fleet (single alien)'''

	def __init__ (self, ai_game):
		'''initialize the alien and set its starting position'''
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		#load the alien image and set its rect attribute
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		#start each new alien near the top left of the screen, leaving space equal to its width and height from the origin (top left)
			#we update the locations in the fleet creation functions
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#store the alien's exact horizontal position (since we would be mainly concerned with precision in horizontal movement, like we are for the player ship)
		self.x = float(self.rect.x)
		pass
	#end init()

	def check_edges (self):
		'''return true if alien is at edge of screen'''
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <=0: 
			#safer to use >= than = coz of any float roundings, current or future
			return True
		pass
	#end def

	def update (self):
		'''move the alien to the right or left'''
		self.x += self.settings.alien_speed * self.settings.fleet_direction
			#recall direction 1 is right and -1 is left
		self.rect.x = self.x
		pass
	#end def 

	pass
#end class
