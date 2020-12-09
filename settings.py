#till version C, file only has static settings. From Version D, has speed scale up and dynamic settings

class Settings:
	'''a class to store all settings for Alien Invasion'''

	def __init__(self):
		'''initialize the game's static settings'''
		# Screen settings
		self.screen_width = 1130 #Book has 1200 by 800, but my monitor has 766 or so height
		self.screen_height = 500
		self.bg_color = (230,230,230)		#is a light gray. Possibly corresponds to Windows LIGHTGRAY

		# Ship settings
		self.ship_limit = 3 #number of lives a player has
		
		# Bullet settings
		self.bullet_width = 3 #default is 3, increase for testing or powerups
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 4 #book original is 3

		# Alien settings
		self.fleet_drop_speed = 10 #original is 10
		#fleet_direction of 1 represents right, -1 left
		self.fleet_direction = 1 #in dynamic version, book for some reason moves this to initialize_dynamic_settings(), but isn't needed, keeping here

		#how quickly the game speeds up
		self.speedup_scale = 1.3 #book original is 1.1
		#how quickly alien points values increase
		self.score_scale = 1.5 #book default is 1.5

		self.initialize_dynamic_settings()
		pass
	#end def


	def initialize_dynamic_settings(self):
		'''initialize settings that change throughout the game'''
		self.bullet_speed = 3.5	#book original is 1.0, but in fullscreen mode, things are slowing down, so making faster
		self.ship_speed = 2.5	#book value is at 1.5, was fine in window, but became slow in full-screen, so bumped up since \
		#version 4 of main file. It gets still faster if use this value in a window
		self.alien_speed = 1.0 #book original is 1, at least on page 286 (where dynamic settings are introduced)

		#scoring
		self.alien_points = 50 #points awarded for shooting first wave aliens, progressively increase, but this is initializer

		pass
	#end def

	def increase_speed(self): #done after each successful round/wave
		'''increase speed settings and alien point values'''
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
		pass
	#end def

	pass
#end class defn

