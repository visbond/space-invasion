import pygame.font #this means the same as 'from pygame import font'

class Button:
	def __init__(self, ai_game, msg):
		'''initialise button attributes'''
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		#set the dimensions and properties of the button
		self.width, self.height = 200,50	#BUILD NOTES: for max portability, should take this as proportion of screen rect
		self.button_color = (0,0,244)	#book has 255 here and below. Has green here, changing to blue because aliens also green
		self.text_color = (244,244,244)
		self.font = pygame.font.SysFont(None,48) #None specifies default font, 48 is size

		#build the button's rect object and center it
		self.rect = pygame.Rect(0,0,self.width,self.height)
		self.rect.center = self.screen_rect.center

		#the button message needs to be prepped only once
		self._prep_msg(msg)
		pass
	#end def init

	def _prep_msg(self, msg):
		'''turn msg into a rendered image and center text on the button'''
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
			#render text as image with spec text and background color. True is for antialiasing
			#if background color is not specified, method tries to render with transparent background, 
			#which should work for us too
		self.msg_image_rect = self.msg_image.get_rect()	#get the above's rect (for below)
		self.msg_image_rect.center = self.rect.center	#match it to button's rect
		pass
	#end def _prep_msg()

	def draw_button(self):
		'''draw blank button and then draw message'''
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
		pass
	#end def draw_button()