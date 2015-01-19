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
		
		self.rusty = rusty.Rusty((5,180))
		self.boxImages = {"metal3": pygame.image.load('mboxbw3.png').convert_alpha(),"metal":pygame.image.load("mbox1.png").convert_alpha(),"cardboard":pygame.image.load("cboxbw.png").convert_alpha()}
		self.objects = []
	def drawBkg(self, imageName = None, rect = None):
		'''Draws the background elements. If it is given a image name, then the background will be filled by the given image'''
		if imageName != None:
			background = pygame.image.load(imageName).convert_alpha()
		if rect == None:
			if imageName == None:
				self.screen.fill((255,255,255))
			else:
				self.screen.blit(background,(0,0))
			self.refresh.append(self.screen.get_rect())
		else:
			if imageName == None:
				self.screen.fill( (255, 255, 255), rect )
			else:

				self.screen.blit(background,rect,rect)
			self.refresh.append( rect )
	def blit(self,obj):
		if obj.rect.right > 0 and obj.rect.left <self.screensize[0]:
			self.screen.blit(obj.image,obj.rect)
	def updateState(self,background=None):
		self.drawBkg(background,self.rusty.rect)
		if self.rusty.rect.right >= self.screensize[0]:
			diffX = self.rusty.rect.left
		elif self.rusty.rect.left < 0:
		 	diffX =  self.rusty.rect.width- self.screensize[0]
		else:
			diffX = 0
		self.rusty.move(self.objects,diffX)
		
		self.screen.blit(self.rusty.image,self.rusty.rect)
		rm = []
		for item in self.objects:
			if item.rect.left <self.screensize[0] and item.rect.right >0:
				self.drawBkg(background,item.rect)
			item.move(self.objects)
			item.location[0] = item.location[0] -diffX
			item.rect = pygame.Rect((item.rect.width/2+item.location[0],item.rect.height/2+item.location[1]),(item.rect.width,item.rect.height))
			self.blit(item)

		pygame.display.update(self.refresh)

		self.refresh = []
	def loadLevel(self, level,background = None):
		metalSize = self.boxImages["metal"].get_rect().width
		metal3Size = self.boxImages["metal3"].get_rect().width
		cardboardSize = self.boxImages["cardboard"].get_rect().width
		self.drawBkg(background)
		self.objects = []
		fp = open(level,'r')
		level = fp.read().split("\r")
		fp.close()
		row = 0
		column = -75

		mCount = 0
		for i in level:
			for obj in i:
				if obj == '.':
					column += metalSize
					mCount = 0
				elif obj == 'm':
					column +=metalSize
					self.objects.append(box.Box([column,row],"metal",self.rusty,self.boxImages))
					if mCount <3:
						mCount +=1
					if mCount == 3:
						mCount = 0
						column -=3*metalSize
						row +=1.5
						self.objects = self.objects[:-3]
						self.objects.append(box.Box([column,row],"metal3",self.rusty,self.boxImages))
						column +=metal3Size
						row -=1.5
				elif obj == 'c':
					column += cardboardSize
					self.objects.append(box.Box([column,row],"cardboard",self.rusty,self.boxImages))
					mCount = 0
			mCount = 0
			column = -75
			row +=50
		self.rusty.reset()
		self.screen.blit(self.rusty.image,self.rusty.rect)
		for item in self.objects:
			self.blit(item)
		pygame.display.update()

	def main(self):
		self.refresh = []
		
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
				self.drawBkg(imageName = "heartPicture.jpeg")
				
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
							self.loadLevel('level1.csv','factory.png')

							
				pygame.display.update(self.refresh)
			
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
							pygame.display.update(self.refresh)
							for item in self.objects:
								item.pickUp()
							pickup.play()
					if event.type == pygame.KEYUP:
						if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
							self.rusty.stop()
						if event.key == pygame.K_SPACE:
							if self.rusty.box != None:
								self.rusty.box.drop()
								
								drop.play()
				if self.rusty.rect.centery >self.screensize[1] :
					#Go back to beginning if dead
					self.rusty.left = False
					self.rusty.speed = [0,0]
					self.rusty.location = [self.rusty.start[0],self.rusty.start[1]+10]
					
					fall.play()
					self.state = 'end'
					pygame.mixer.music.load('AllThis.mp3')
					soundstate = 'play'

				self.updateState('factory.png')

				# throttle the game speed to 30fps
				self.clock.tick(120)
			
			if self.state == "end":
				'''Creates a game over page'''
				self.drawBkg()	
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
											
				pygame.display.update(self.refresh)			

				
			if self.state == "credits":
				'''Creates a credits page'''
				credits = []
				self.drawBkg()

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
				resources.append(afont.render("Bruce: http://cs.colby.edu/maxwell/", True, (0,0,0)))
				resources.append(afont.render("Music: Kevin Macleod at http://incompetech.com/",True,(0,0,0)))
				resources.append(afont.render("Sounds: GarageBand", True, (0,0,0)))
				for i in range(len(resources)):
					self.screen.blit(resources[i],(10,resourcesLoc+110+20*i))

				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							self.state = "thanks"
							pygame.mixer.music.load('spazzmaticpolka.mp3')
							soundstate = "play"
				pygame.display.update(self.refresh)
				
			if self.state == "thanks":
				self.drawBkg()
				bruce = pygame.image.load( "Bruce-Header-Collage.png" ).convert_alpha()
				self.screen.blit( bruce, (220, 200) )
				afont = pygame.font.SysFont("Arial", 40)
				title = afont.render("Special Thanks To",True,(0,0,0))
				self.screen.blit(title,(150,30))

				afont = pygame.font.SysFont("Arial", 40)
				name = afont.render("Professor Bruce Maxwell",True,(0,0,0))
				self.screen.blit(name,(100,100))
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						sys.exit()
				pygame.display.update(self.refresh)


if __name__ == '__main__':
	game = RustyHeart()
	game.main()



			







