import sys
import random
import rusty
import pygame

class RustyHeart:
	def __init__(self):
		self.rusty = rusty.Rusty((0,400),(0,0), "stationary" )
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
		
	def drawBkg(self, refresh,imageName = None, rect = None):
		if imageName != None:
			background = pygame.image.load(imageName).convert_alpha()
		if rect == None:
			if imageName == None:
				self.screen.fill((255,255,255))
			else:
				self.screen.blit(background,(0,0))
			refresh.append(self.screen.get_rect())
		else:
			if imageName == None:
				self.screen.fill( (255, 255, 255), rect )
			else:
				self.screen.blit(background,(0,0),rect)
			refresh.append( rect )

	def main(self):
		refresh = []
		self.drawBkg(refresh)
		pygame.display.update()
		while self.state == "start":
			self.drawBkg(refresh, imageName = "heartPicture.jpeg")
			
			afont = pygame.font.SysFont("Arial", 72)
			title = afont.render("Rusty Heart",True,(155,50,50))
			self.screen.blit(title,(140,150))

			afont = pygame.font.SysFont("Times New Roman", 20, italic = True, bold = True)
			space = afont.render("press SPACE to continue", True, (155,50,50))
			self.screen.blit(space,(200,250))

			quit = afont.render("press q to quit", True, (155,50,50))
			self.screen.blit(quit,(250,300))
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						sys.exit()
					if event.key == pygame.K_SPACE:
						#refresh = []
						self.state = "sandbox"
						#break
			pygame.display.update(refresh)
		while self.state == "sandbox":
			self.drawBkg(refresh)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						sys.exit()
			pygame.display.update(refresh)
		
			
if __name__ == '__main__':
	game = RustyHeart()
	game.main()



			







