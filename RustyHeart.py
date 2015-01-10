import sys
import random
import rusty
import pygame

class RustyHeart:
	def __init__(self):
		self.rusty = new rusty.Rusty((0,400),(0,0), "stationary" )
		self.state = "start"
		pygame.init()

		self.screensize = (640,480)
		#set up fonts
		try:
			pygame.font.init()
		except:
			print "Fonts unavailable"
			sys.exit()
		#set up clock
		self.clock = pygame.time.Clock()
		#create screen
		self.screen = pygame.display.set_mode(self.screensize)
		
	def drawBkg(self,screen, refresh, text = None, imageName = None, rect = None):
			if imageName != None:
				background = pygame.image.load(imageName).convert_alpha()
			if rect == None:
				if imageName == None:
					self.screen.fill((255,255,255))
				else:
					self.screen.blit(background,(-30,-30))
				if text != None:
					self.screen.blit(text,(10,10))
				refresh.append(screen.get_rect())
			else:
				if imageName == None:
					self.screen.fill( (255, 255, 255), rect )
				else:
					self.screen.blit(background(-30,-30))

				# blit the text surface onto the screen if it is inside the rectangle
				if text != None:
					self.screen.fill( (255, 255, 255), text.get_rect().move(10, 10).clip( rect ) )

					trect = text.get_rect().move(10, 10) # rectangle in which to
												 # draw the text						 
					clippedRect = trect.clip( rect ) # intersection of the text
											 # screen rectangle and the
											 # area to update
					# blit the text into the area to update, the second rectangle
					# indicates which part of the text to use
					urect = screen.blit( text, clippedRect, clippedRect.move(-10,-10) )

				# refresh the rectangle
				refresh.append( rect )




			







