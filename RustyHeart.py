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
		
		self.rusty = rusty.Rusty([50,180])
		self.boxImages = {"metal":pygame.image.load("mbox.png").convert_alpha(),"cardboard":pygame.image.load("cbox.png").convert_alpha()}
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
		cboxes = []
		mboxes = []
		self.drawBkg(refresh)
		pygame.display.update()
		
		soundstate = "start"
		pygame.mixer.music.load('start.mp3')
		pygame.mixer.music.play(-1)
		jump = pygame.mixer.Sound( "jumping.wav" )
		jump.set_volume(0.05)
		pickup = pygame.mixer.Sound( "pickup.wav" )
		pickup.set_volume(0.05)
		drop = pygame.mixer.Sound( "drop.wav" )
		drop.set_volume(0.05)
		fall = pygame.mixer.Sound( "falling.wav" )
		fall.set_volume(0.1)
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
				space = afont.render("press ENTER to play", True, (155,50,50))
				self.screen.blit(space,(210,260))

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
							mboxes.append(box.Box([-100,300],"metal",self.rusty,self.boxImages))
							mboxes.append(box.Box([100,150],"metal",self.rusty,self.boxImages))
							cboxes.append(box.Box([100,240],"cardboard",self.rusty,self.boxImages))
							
							
							self.screen.blit( self.rusty.image, self.rusty.rect )
							for i in range(len(mboxes)):
								self.screen.blit(mboxes[i].image, mboxes[i].rect)
							for i in range(len(cboxes)):
								self.screen.blit( cboxes[i].image, cboxes[i].rect)
							
							pygame.display.update()
				pygame.display.update(refresh)
			
			if self.state == "sandbox":
				for event in pygame.event.get():
					#Handles key presses
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							self.state = "end"
							pygame.mixer.music.load('AllThis.mp3')
							soundstate = 'play'

						if event.key == pygame.K_LEFT:
							self.rusty.speedLeft()
						if event.key == pygame.K_RIGHT:
							self.rusty.speedRight()
						if event.key == pygame.K_UP:
							self.rusty.jump()
							
							jump.play()
						if event.key == pygame.K_SPACE:
							pygame.display.update(refresh)
							for i in range(len(cboxes)):
								cboxes[i].pickUp()
							pickup.play()
					if event.type == pygame.KEYUP:
						if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
							self.rusty.stop()
						if event.key == pygame.K_SPACE:
							if self.rusty.box != None:
								self.rusty.box.drop()
								
								drop.play()
				if self.rusty.rect.centery >480 :
					#Go back to beginning if dead
					self.rusty.left = False
					self.rusty.speed = [0,0]
					self.rusty.location = [self.rusty.start[0],self.rusty.start[1]+10]
					
					fall.play()
					self.state = 'end'
					pygame.mixer.music.load('AllThis.mp3')
					soundstate = 'play'
					

				self.drawBkg(refresh,'factory.png',self.rusty.rect)
				
				#handling collisions
				for i in range(len(mboxes)):
					self.drawBkg(refresh,'factory.png',mboxes[i].rect)
					'''#handle collision when not jumping
					if (not self.rusty.justJumped and self.rusty.rect.colliderect(mboxes[i].rect) and ((self.rusty.image==self.rusty.leftImage and self.rusty.location[0]>mboxes[i].location[0]+mboxes[i].rect.width) or (self.rusty.image==self.rusty.rightImage and self.rusty.location[0]<mboxes[i].location[0]+mboxes[i].rect.width))):
						self.rusty.speed[0] = 0
					#handle collision when jumping
					collisionBox = self.rusty.rect.move((self.rusty.rect.width/2)*self.rusty.speed[0],-abs((self.rusty.rect.height/2)*self.rusty.speed[1]))
					if (self.rusty.justJumped and self.rusty.location[1]>=mboxes[i].location[1] and collisionBox.colliderect(mboxes[i])):
						self.rusty.justJumped = False
						self.rusty.speed[0] = 0'''
				for i in range(len(cboxes)):
					self.drawBkg(refresh,'factory.png',cboxes[i].rect)
					if(not self.rusty.justJumped and self.rusty.rect.colliderect(cboxes[i].rect) and ((self.rusty.image==self.rusty.leftImage and self.rusty.location[0]>cboxes[i].location[0]) or (self.rusty.image==self.rusty.rightImage and self.rusty.location[0]<cboxes[i].location[0]))):
						self.rusty.speed[0] = 0
				allboxes = []
				allboxes = cboxes+mboxes
				self.rusty.move(allboxes)
				for i in range(len(cboxes)):
					cboxes[i].move(mboxes)

				self.rusty.rect = pygame.Rect((self.rusty.rect.width/2+self.rusty.location[0],self.rusty.rect.height/2+self.rusty.location[1]),(self.rusty.rect.width,self.rusty.rect.height))
				for i in range(len(mboxes)):
					mboxes[i].rect = pygame.Rect((mboxes[i].rect.width/2+mboxes[i].location[0],mboxes[i].rect.height/2+mboxes[i].location[1]),(mboxes[i].rect.width,mboxes[i].rect.height))
				for i in range(len(cboxes)):
					cboxes[i].rect = pygame.Rect((cboxes[i].rect.width/2+cboxes[i].location[0],cboxes[i].rect.height/2+cboxes[i].location[1]),(cboxes[i].rect.width,cboxes[i].rect.height))
			
				self.screen.blit(self.rusty.image,self.rusty.rect)
				refresh.append(self.rusty.rect)
				for i in range(len(mboxes)):
					self.screen.blit(mboxes[i].image,mboxes[i].rect)
					refresh.append(mboxes[i].rect)
				for i in range(len(cboxes)):
					self.screen.blit(cboxes[i].image,cboxes[i].rect)
					refresh.append(cboxes[i].rect)

				# update the parts of the screen that need it			
				pygame.display.update(refresh)

				# clear out the refresh rects
				refresh = []

				# throttle the game speed to 30fps
				self.clock.tick(30)
			
			if self.state == "end":
				'''Creates a game over page'''
				self.drawBkg(refresh)	
				afont = pygame.font.SysFont("Times New Roman", 50)
				title = afont.render("Game Over",True,(0,0,0))
				self.screen.blit(title,(210,20))
				
				rusty = pygame.image.load( "rustysmall.png" ).convert_alpha()
				self.screen.blit( rusty, (195, 100) )
				
				afont = pygame.font.SysFont("Times New Roman", 20, italic = True, bold = True)
				space = afont.render("press ENTER for new game", True, (155,50,50))
				self.screen.blit(space,(210,360))

				quit = afont.render("press q to quit", True, (155,50,50))
				self.screen.blit(quit,(265,390))
				
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
				self.screen.blit(title,(10,0))

				afont = pygame.font.SysFont("Lucida Console", 18)
				credits.append(afont.render("Producer: .......................Beatrice Liang", True,(0,0,0)))
				credits.append(afont.render("Designer: .......................Luis Henriquez-Perez", True,(0,0,0)))
				credits.append(afont.render("Lead Programmer: ................Itrat Akhter", True,(0,0,0)))
				credits.append(afont.render("Lead Visual Artist: .............Catherine Alden", True,(0,0,0)))
				credits.append(afont.render("Lead Audio Artist: ..............Tiffany Lam", True,(0,0,0)))
				credits.append(afont.render("Quality Assurance Specialist: ...Shama Ramos", True,(0,0,0)))
				resourcesLoc = 50
				for i in range(len(credits)):
					resourcesLoc += 25
					self.screen.blit(credits[i], (20,resourcesLoc))

				afont = pygame.font.SysFont("Arial", 50)
				title = afont.render("Resources", True,(0,0,0))
				self.screen.blit(title,(10,resourcesLoc+40))

				resources = []
				afont = pygame.font.SysFont("Lucida Console", 15)
				resources.append(afont.render("Start Screen Image: https://www.flickr.com/photos/seanfx/", True,(0,0,0)))
				resources.append(afont.render("Songs: Kevin Macleod at http://incompetech.com/",True,(0,0,0)))
				for i in range(len(resources)):
					self.screen.blit(resources[i],(10,resourcesLoc+110+20*i))

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



			







