#This is from Version F, some modifications to display ships remaining on screen

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
	'''a class to report scoring information'''

	def __init__(self, ai_game):
		'''initialize scorekeeping attributes'''
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		#font settings for scoring information
		self.text_color = (30,30,30) #a fairly dark gray
		self.font = pygame.font.SysFont(None, 48) #None indicates default font, 48 is size
		
		#prepare the initial score image
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
		pass
	#end def init

	def prep_score(self):
		'''turn the score into a rendered image'''
		#score_str = str(self.stats.score) #original version
		score_str = "{:,}".format(self.stats.score) #later version (also from book, minor modification; not rounding score to nearest 10)

		self.score_image = self.font.render(score_str, True,
			self.text_color, self.settings.bg_color)

		#display the score at the top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20 #set right edge of scorebox 20 pixels\
		#in from right edge of screen. As number gets larger, it will grow to the left, right edge is anchored
		self.score_rect.top = 20
		pass
		#note this method prepares the image but does not display it, that's show_score()
	#end def prep_score()

	def prep_high_score(self):
		'''turn the high score into a rendered image'''
		high_score_str = "{:,}".format(self.stats.high_score) #this is to put comma separators. Skipping rounding to nearest 10, which book does (round(num,-1))
		high_score_str = "HI " + high_score_str	#my addition, so is clear is high score
		self.high_score_image = self.font.render(high_score_str, True,
			self.text_color, self.settings.bg_color)

		#center the high score at the top of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top
		pass
	#end def

	def prep_level(self):
		'''turn the level into a rendered image'''
		level_str = "Lvl" + str(self.stats.level) #the "Lvl" prefix is my addition,\
		#to make it clear to player what this number is
		self.level_image = self.font.render(level_str, True,
			self.text_color, self.settings.bg_color)

		#position the level below the score.
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right #ERROR LESSON: had typo-ed - instead of = here. Level was displaying but at wrong location
		self.level_rect.top = self.score_rect.bottom + 10
		pass
	#end def prep_level()

	def prep_ships(self):
		'''show how many ships are left'''
		self.ships = Group() #start with an empty group
		for ship_number in range (self.stats.ships_left):
			#for each ship player has left, initialise a ship object, set position, and add to above group
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship) 
		pass
	#end def prep_ships()

	def show_score(self):
		'''draw scores, level, and ships to the screen'''
		#note that all of these are inbuilt methods
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen) #call inbuilt draw method on the sprite group
		pass
	#end def show_score()

	def check_high_score(self):
		'''check to see if there's a new high score'''
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()
		pass
	#end def



	pass
#end class def