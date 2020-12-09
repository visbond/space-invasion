#this applies to version F. (shows remaining ships at top left graphically, so now inherits from Sprite)
#Till Version E have saved that file separately

import pygame
from pygame.sprite import Sprite

class Ship(Sprite): 
	'''a class to manage the ship'''
	#without inheriting from Sprite, Ship won't have methods for adding sprites, which are being used in Scoreboard to display ship images
	def __init__ (self, ai_game):
		'''initialize the ship and set its starting position'''
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		#load the ship image and get its rect
		self.image = pygame.image.load('images/ship.bmp') #ERROR LESSON: hadn't used quotes in argument earlier, got Name error, that name images is not defined. Arg must be string with pathname
		self.rect = self.image.get_rect()

		#start each ship at the middle bottom of the screen
		self.rect.midbottom = self.screen_rect.midbottom	

		#store a decimal value for the ship's horizontal position. rect coordinates are int by default, but we want
		#to allow for decimals, because ship speed may have fine gradations. So explicity float() cast
		self.x = float(self.rect.x)

		#movement flags
		self.moving_right = False
		self.moving_left = False

		pass
 	#end init def

	def blitme (self):
		self.screen.blit(self.image,self.rect)
		pass
	#end def

	def update(self):
		'''updates the ship's position based on the movement flags'''
		#update the ship's x-value now, not directly the rect
		if self.moving_right and self.rect.right<self.screen_rect.right: #the second part ensures the ship doesn't move off the edge of the screen
			#self.rect.x += 1
			self.x += self.settings.ship_speed
			
		#elif self.moving_left: #ref long comment below. Do try the elif version if haven't yet, is instructive. Try pressing both keys and pressing in quick succession with some simultaneous press (have saved that main and ship file separately)
		if self.moving_left and self.rect.left>0: #the part after the and ensures ship doesn't go off the edge
			#self.rect.x -= 1
			self.x -= self.settings.ship_speed
# from the book, P. 240 (PDF page 278): In update(), we use two separate if blocks rather than an elif to allow the ship’s rect.x value to be
# increased and then decreased when both arrow keys are held down. This results in the ship standing still. If we used elif for motion to the left, the
# right arrow key would always have priority. Doing it this way makes the movements more accurate when switching from right to left when the player
# might momentarily hold down both keys. 
	
		#now update rect object from the stored value of x (would take integer part of the float)
		self.rect.x = self.x
		pass
	#end def

	def center_ship(self):
		'''center the ship on the screen. Usually needed after a ship is destroyed
			and a new one is to be placed on the screen'''
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x) #self.x is being used by us to do precise (float) tracking of ship movement (allows for fine decimal speed scale ups and downs, though drawing would always be rounded or truncated to nearest int pixel)
		pass
	#end def