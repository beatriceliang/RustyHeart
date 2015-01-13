import sys
import random
import rusty
import pygame
import box

class RustyHeart:
	def __init__(self):
		'''Creates an instance of Rusty, initializes pygame'''
		
		self.state = "start"
		pygame.init()

		self.screensize = (640,479)
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
		
		self.rusty = rusty.Rusty()
	def drawBkg(self, refresh,imageName = None, rect = None):
		'''Draws the background elements. If it is given a image name, then the background will be filled by the given image'''
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

				self.screen.blit(background,rect,rect)
			refresh.append( rect )

	def main(self):
		refresh = []
		self.drawBkg(refresh)
		pygame.display.update()
		
		soundstate = "start"
		pygame.mixer.music.load('start.mp3')
		pygame.mixer.music.play(-1)

		while True:
			if soundstate == "play":
				pygame.mixer.music.play(-1)
				soundstate = "start"
			if self.state == "start":
				'''Creates the start screen'''
				soundstate == "play"
				self.drawBkg(refresh, imageName = "heartPicture.jpeg")
				
				afont = pygame.font.SysFont("Arial", 72)
				title = afont.render("Rusty Heart",True,(155,50,50))
				self.screen.blit(title,(140,150))

				afont = pygame.font.SysFont("Times New Roman", 25, italic = True, bold = True)
				space = afont.render("press enter to play", True, (155,50,50))
				self.screen.blit(space,(215,260))

				quit = afont.render("press q to quit", True, (155,50,50))
				self.screen.blit(quit,(240,300))
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							sys.exit()
						if event.key == pygame.K_RETURN:
							self.state = "sandbox"
							pygame.mixer.music.load('chaos.mp3')
							soundstate = "play"

							self.drawBkg(refresh,'factory.png')
							mbox = box.Box([-100,400],"metal",self.rusty)
							cbox = box.Box([100,340],"cardboard",self.rusty)
							self.screen.blit( self.rusty.image, self.rusty.rect )
							self.screen.blit( mbox.image, mbox.rect)
							self.screen.blit( cbox.image, cbox.rect)
							pygame.display.update()
				pygame.display.update(refresh)
			
			if self.state == "sandbox":
				
				for event in pygame.event.get():
					#Handles key presses
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							sys.exit()
						if event.key == pygame.K_n:
							self.state = "credits"
							pygame.mixer.music.load('radiomartini.mp3')
							soundstate = "play"

						if event.key == pygame.K_LEFT:
							self.rusty.speedLeft()
						if event.key == pygame.K_RIGHT:
							self.rusty.speedRight()
						if event.key == pygame.K_UP:
							self.rusty.jump()
							jump = pygame.mixer.Sound( "jumping.wav" )
							jump.play()
						if event.key == pygame.K_SPACE:
							pygame.display.update(refresh)
							cbox.pickUp()
							pickup = pygame.mixer.Sound( "pickup.wav" )
							pickup.play()
					if event.type == pygame.KEYUP:
						if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
							self.rusty.stop()
						if event.key == pygame.K_SPACE:
							if self.rusty.box != None:
								self.rusty.box.drop()
								drop = pygame.mixer.Sound( "drop.wav" )
								drop.play()
				if self.rusty.rect.centery >480 :
					#Go back to beginning if dead
					fall = pygame.mixer.Sound( "falling.wav" )
					fall.play()
					self.state = 'end'
					pygame.mixer.music.load('AllThis.mp3')
					soundstate = 'play'
					self.rusty.left = False
					self.rusty.speed = [0,0]
					self.rusty.location = [50,200]

				self.drawBkg(refresh,'factory.png',self.rusty.rect)
				self.drawBkg(refresh,'factory.png',mbox.rect)
				self.drawBkg(refresh,'factory.png',cbox.rect)

				self.rusty.move([cbox,mbox])
				cbox.move([mbox])

				self.rusty.rect = pygame.Rect((self.rusty.rect.width/2+self.rusty.location[0],self.rusty.rect.height/2+self.rusty.location[1]),(self.rusty.rect.width,self.rusty.rect.height))
				mbox.rect = pygame.Rect((mbox.rect.width/2+mbox.location[0],mbox.rect.height/2+mbox.location[1]),(mbox.rect.width,mbox.rect.height))
				cbox.rect = pygame.Rect((cbox.rect.width/2+cbox.location[0],cbox.rect.height/2+cbox.location[1]),(cbox.rect.width,cbox.rect.height))
				
				self.screen.blit(self.rusty.image,self.rusty.rect)
				refresh.append(self.rusty.rect)
				self.screen.blit(mbox.image,mbox.rect)
				refresh.append(mbox.rect)
				self.screen.blit(cbox.image,cbox.rect)
				refresh.append(cbox.rect)

				# update the parts of the screen that need it			
				pygame.display.update(refresh)

				# clear out the refresh rects
				refresh = []

				# throttle the game speed to 30fps
				self.clock.tick(30)
			
			if self.state == "end":
				'''Creates a game over page'''
				self.drawBkg(refresh)	
				afont = pygame.font.SysFont("Arial", 50)
				title = afont.render("Game Over",True,(0,0,0))
				self.screen.blit(title,(0,0))
				
				afont = pygame.font.SysFont("Times New Roman", 20, italic = True, bold = True)
				space = afont.render("press ENTER for new game", True, (155,50,50))
				self.screen.blit(space,(210,260))

				quit = afont.render("press q to quit", True, (155,50,50))
				self.screen.blit(quit,(255,300))
				
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							self.state = "credits"
							pygame.mixer.music.load('radiomartini.mp3')
							soundstate = "play"
						if event.key == pygame.K_RETURN:
							self.state = "start"
							pygame.mixer.music.load('start.mp3')
							soundstate = "play"
											
				pygame.display.update(refresh)			

				
			if self.state == "credits":
				'''Creates a credits page'''
				credits = []
				self.drawBkg(refresh)

				afont = pygame.font.SysFont("Arial", 50)
				title = afont.render("Credits",True,(0,0,0))
				self.screen.blit(title,(0,0))

				afont = pygame.font.SysFont("Lucida Console", 20)
				credits.append(afont.render("Producer: .......................Beatrice Liang", True,(0,0,0)))
				credits.append(afont.render("Designer: .......................Luis Henriquez-Perez", True,(0,0,0)))
				credits.append(afont.render("Lead Programmer: ................Itrat Akhter", True,(0,0,0)))
				credits.append(afont.render("Lead Visual Artist: .............Catherine Alden", True,(0,0,0)))
				credits.append(afont.render("Lead Audio Artist: ..............Tiffany Lam", True,(0,0,0)))
				credits.append(afont.render("Quality Assurance Specialist: ...Shama Ramos", True,(0,0,0)))
				resourcesLoc = 50
				for i in range(len(credits)):
					resourcesLoc += 25
					self.screen.blit(credits[i], (0,resourcesLoc))

				afont = pygame.font.SysFont("Arial", 50)
				title = afont.render("Resources", True,(0,0,0))
				self.screen.blit(title,(0,resourcesLoc+40))

				resources = []
				afont = pygame.font.SysFont("Lucida Console", 15)
				resources.append(afont.render("Start Screen Image: https://www.flickr.com/photos/seanfx/", True,(0,0,0)))
				resources.append(afont.render("Songs: Kevin Macleod at http://incompetech.com/",True,(0,0,0)))
				for i in range(len(resources)):
					self.screen.blit(resources[i],(0,resourcesLoc+110+20*i))

				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							sys.exit()
						if event.key == pygame.K_SPACE:
							self.state = "thanks"
							pygame.mixer.music.load('spazzmaticpolka.mp3')
							soundstate = "play"
				pygame.display.update(refresh)
			if self.state == "thanks":
				self.drawBkg(refresh)

				afont = pygame.font.SysFont("Arial", 50)
				title = afont.render("Special Thanks To",True,(0,0,0))
				self.screen.blit(title,(0,0))

				afont = pygame.font.SysFont("Arial", 70)
				name = afont.render("Professor Bruce Maxwell",True,(0,0,0))
				self.screen.blit(name,(0,50))
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						sys.exit()
				pygame.display.update(refresh)


if __name__ == '__main__':
	game = RustyHeart()
	game.main()



			







