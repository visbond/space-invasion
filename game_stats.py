class GameStats:
	'''track statistics for Alien Invasion'''

	def __init__(self, ai_game):
		'''initialize statistics'''
		self.settings = ai_game.settings
		#high score. It is never reset in one game session
		self.high_score = 0		
		self.reset_stats() #called once in the beginning (with this constructor), and also whenever a new game is started (in the same program instance)
		#start Alien Invasion in an inactive state.
		self.game_active = False
		pass
	#end def

	def reset_stats(self):
		'''initialize statistics that can change during the game'''
		self.ships_left = self.settings.ship_limit
		self.score = 0	#score should reset to 0 for each new game
		self.level = 1 #player's level
		pass
	#end def