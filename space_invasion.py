#continues Alien Invasion, basic features were implemented till version A, which does till end of Chap 13 of
# the book (Python Crash Course by Eric Matthes)
#version E, continue from Chap 14. page 299. Add ships remaining graphic
#prev version C added Ex 14-1 suggestion, can press P to play.
#traverse collision dictionary to accommodate wide bullets that kill multiple aliens at once.
#in addition to book code, added code to quit game when press Esc key (keycode 27), along with the extant 'q' key -- note that the Windows Cross button is no longer available when in full-screen mode, and Pygame has no defined way to quit then

#TODOs later: (low-hanging are ##)
#speed scaler, can choose fast/slow speed via cline args and/or initial menu. Eventually use timers to standardise
#sprite scaling based on screen size and exact number of sprites per appearance, independent of screen size (can have 3 sizes of pre-rendered sprites for different screens)
#sounds and music
#for menu, can try default font on various systems, else embed free font
##nebula type background.(have assets by DinV)
#timtim stars on background (have downloaded assets by DinV)
#3 stages with different backgrounds, harder speed and tougher enemies (with different sprites)
#"Dragon" at end of each stage
#can have two or three different hardness enemies, take multiple bullets
#enemies drop bombs
##powerups that give 'laser' bullets occasionally (code already known, just change collision first bool arg to False)
#.
#long-run, full scrolling platformer like 1942

import sys
from time import sleep #as of now (version 9) only used to pause the game for a moment when the ship is hit

import pygame

from settings import Settings	#user-defined modules
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	'''overall class to manage game assets and behaviour'''

	def __init__(self): #ERROR LESSON: did single instead of double underscores around init(), got no error or exception in compilation, just later runtime errors about display not initialized, display mode not set etc.
		
		'''initialize the game and create game resources'''
		pygame.init() #from stack overflow etc, learned that there are init() methods for many subsystems \
		#(such as pygame.display.init()), but calling this global init() does a lot of the basic stuff for \
		#multiple subsystems automatically so is more convenient (though would also init things which we \
		#might not need, so if have some sort of time-critical use-case, being specific might be better)

		self.settings = Settings() #import settings from external module
		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #note double brackets, needs tuple argument. 
		#above: By assigning to attribute self.screen, this display window becomes available to all methods of the class
		#(it is a 'surface', in this case being the entire display window)
		self.settings.screen_width,self.settings.screen_height = self.screen.get_rect().width, self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		#create an instance to store game statistics, 
		#and create a scoreboard
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)	#note this self will translate to the second argument of Ship's constructor, which is ai_game instance
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()

		#make the play button
		self.play_button = Button(self,"Click Here or Press P to Play") #makes button but its draw call is made in _update_screen()
		pass
	#end def

	def run_game(self):
		'''start the main loop for the game'''
		#this while loop will contain an event loop (a for loop), and additional code to manage the display
		#will refer to this outer while as the mainloop
		while True:
			#watch for keyboard and mouse events /event loop
			self._check_events()

			if self.stats.game_active: #if play is active, i.e. not in game over state
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			
			self._update_screen()
		#end while
		pass
	#end def

	def _check_events(self):
		'''event loop, called by mainloop'''
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #this happens in windowed game, when user presses cross at top-right, so practically not in use right now
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN: #check if user presses play button
				mouse_pos = pygame.mouse.get_pos() #returns x,y coordinate tuple
				self._check_play_button(mouse_pos)
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

		#end for
		pass
	#end def

	def _check_play_button(self, mouse_pos):
		'''start a new game when the player clicks the Play button'''
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active: #second condition is needed, else game restarts even if user presses on (invisible) button during play
			self._start_game()#this has been added acc to Exercise 14-1, code is not given in main text
			#from page 287 (dynamic speeds), initialize_dynamic_settings() is called here, have done in _start_game() now
		pass
	#end def

	def _start_game(self): 
		'''resets and starts the game. Can be called on clicking play button, or pressing P.
		This has been added acc to Exercise 14-1, code is not given in main text'''
		self.stats.reset_stats()	#reset the game (clear aliens, reset player lives etc)
		self.settings.initialize_dynamic_settings() #reset any speedups back to initial values
		self.stats.game_active = True
		self.sb.prep_score() #reset score to 0 (note that high score is not reset, is persistent; declared once in Scoreboard)
		self.sb.prep_level() #reset level to 1
		self.sb.prep_ships() #ships remaining
		#hide the mouse cursor
		pygame.mouse.set_visible(False)

		#get rid of any remaining aliens and bullets (using inbuilt sprite group command)
		self.aliens.empty()
		self.bullets.empty()

		#create a new fleet and center the ship
		self._create_fleet()
		self.ship.center_ship()
		pass
	#end def _start_game	

	def _check_keydown_events(self, event):
		'''respond to keypresses'''
		if event.key == pygame.K_RIGHT:
			#old version comment: move the ship to the right
			#self.ship.rect.x += 1	#note the sprite is not being changed, only the rectangle it is blitted in is being moved
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT: #ref to comment in ship.update() method: we can use elif instead of if here, since the keypresses would always be both read by pygame.get, even if they happen simultaneously
			self.ship.moving_left = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_p and not self.stats.game_active:	#this has been added acc to Exercise 14-1, code is not given in main text
			self._start_game()
		elif event.key == pygame.K_q or event.key == 27: #q is the 'q' key. 27 is the escape key, don't know the pygame.K_ equivalent yet
			sys.exit()
		
		pass
	#end def

	def _check_keyup_events(self, event):
		'''respond to key releases'''
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
		pass
	#end def

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets."""
		# Update bullet positions.
		self.bullets.update() #from book: you call update() on a group, the group automatically calls
				#update() for each sprite in the group. The line self.bullets.update() calls bullet.update() for each bullet we place in the group bullets.
		
		# Get rid of bullets that have disappeared. (else game keeps track of them even though not visible, eats memory)
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		#print(len(self.bullets)) #was for debugging
		self._check_bullet_alien_collisions()		
		pass
	#end def

	def _check_bullet_alien_collisions(self):
		'''Check for any bullets that have hit aliens
			#if they have, get rid of both'''
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
			#above returns a dictionary of all rect collisions; bullets are keys, aliens values
			#the last two arguments remove both collider & collidee. 
			#For laser bullets that kill multiple aliens and reach the top of the screen \
				#set the first Boolean arg to False and second to True
		
		if collisions: #book code assumes one bullet hits one alien. But wide bullet can hit more.\
		#updating this to traverse each value in dictionary (not key, which is bullet; value is alien)
		#this is also important for any future special power bullets that kill multiple aliens
			#print(collisions)	#remember that print() calls should only be used for temporary debugging, as slow the game down due to stdout() branches
			#print(collisions.values())
			#print(list(collisions.values()))
			for alist in collisions.values(): #turns out is a nested list, \
			#so initially used double for loop (one bullet kills multiple aliens, all of them are one list of values with that bullet key)
			#then found is explained in next page of book. Just using len() does the same job
				#print(alist)
				#for alien in alist:
				#	print(alien)
				#	self.stats.score += self.settings.alien_points
				self.stats.score += self.settings.alien_points * len(alist)
			self.sb.prep_score()
			self.sb.check_high_score()

		#if aliens are gone, create a new fleet \
		#[BUILD NOTES: have a setting for a finite number of fleets, \
		#each faster than the last. Player speed can be increased in parallel]
		if not self.aliens: #no objects remain in group
			#destroy existing bullets and create new fleet
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed() #key to making it feel like a game, a challenge

			#Increase level
			self.stats.level += 1
			self.sb.prep_level()
		pass
	#end def

	def _ship_hit(self):
		'''respond to the ship being hit by an alien'''
		if self.stats.ships_left>0:
			#decrement ships left, and update scoreboard (top left ships remaining display)
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			#get rid of any remaining aliens and bullets
			self.aliens.empty()	 #these are inbuilt sprite method calls
			self.bullets.empty()

			#create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#pause
			sleep(0.5)
		else:
			self.stats.game_active = False	#game over
			pygame.mouse.set_visible(True) #show cursor again, so user can click on Play button (button is made in _update_screen())
		pass
	#end def

	def _update_aliens(self):
		'''Check if the fleet is at an edge, then
		update the positions of all aliens in the fleet'''
		self._check_fleet_edges()
		self.aliens.update() #calls the sprite group inbuilt update() method

		#look for alien-ship collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
			#print("Ship hit!!")	#debug msg for now, will take action if this found to work.
	
		#look for any aliens hitting the bottom of the screen, and respond same as ship hit (done inside function)
		self._check_aliens_bottom()
		pass
	#end def

	def _create_fleet(self):
		'''create the fleet of aliens'''
		#make an alien, this one is just for calculations and won't be added to the fleet. 
			#Is local var, would be destroyed on function exit anyway
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size #apparently returns an x,y tuple
		#find the number of aliens that will fit in a row
		#spacing between aliens is one alien width
		alien_width = alien.rect.width #just for convenience, can use rect attrib again and again too
		available_space_x = self.settings.screen_width - (2*alien_width) #leaving a margin of one width at each side
		number_aliens_x = available_space_x // (2*alien_width)

		#determine the height and number of rows that will fit the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height) #leave one alien space at top, and two above the player ship
		number_rows = available_space_y // (2*alien_height)

		#create the fleet of aliens
		for row_number in range (number_rows):
			for alien_number in range (number_aliens_x):
				self._create_alien(alien_number, row_number)
		pass
	#end def

	def _create_alien(self, alien_number, row_number):
		#create an alien 
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size #apparently returns an x,y tuple
		#and place it in the row at the correct location relative to its brethren
		alien.x = alien_width + 2*alien_width * alien_number
		alien.rect.x = alien.x #ERROR LESSON: had forgotten this, all aliens were drawn on top of each other, so apparently only one was visible.
		#Note that rect is the real variable used by the system (why? we only assign get_rect()'s result to it. Something to do with they getting attached by reference?).
		#the plain x is for our convenience (we have made it to be a float)
		alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number #recall origin is top left, so this will move downwards
		self.aliens.add(alien)	#note that aliens has already been created as a sprite group in the aliens constructor
		pass
	#end def

	def _check_aliens_bottom(self):
		'''check if any aliens have reached the bottom of the screen'''
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom: #recall origin is top left, and y increases downward
				#treat this the same as if the ship got hit
				self._ship_hit()
				break #if any one alien reached the bottom, there's no need to check the rest, so break
		#end for
		pass
	#end def				

	def _check_fleet_edges (self):
		'''respond if any aliens have reached the edge'''
		#note this seems wasteful at first, since should only check the left/right edge aliens instead of all\
		#of them, but after a few are shot down, hard to track who are the outermost ones without using many more variables
		for alien in self.aliens.sprites():
			if alien.check_edges():	#if any alien has reached an edge, flip direction
				self._change_fleet_direction()
				break
		pass
	#end def

	def _change_fleet_direction(self):
		'''drop the entire fleet and change direction'''
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1 #toggle direction var for entire fleet
		pass
	#end def

	def _update_screen(self):
		#redraw the screen surface (update images) and flip to the display screen
		self.screen.fill(self.settings.bg_color)		#takes only one argument, a color, and fills the entire object (surface) with it
		self.ship.blitme()		
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)	#note aliens is a sprite group. draw() is an inbuilt function

		#draw the score information
		self.sb.show_score()

		#draw the play button if the game is inactive. 
			#This is being drawn after all the above, so is visible over other elements
		if not self.stats.game_active:
			self.play_button.draw_button()

		#make the most recently drawn screen visible {frame buffer flipped to screen, screen comes to buffer}
		pygame.display.flip()
		pass
	#end def

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
		pass
	#end def

pass
#end class defn



if __name__ == '__main__':
	#make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()