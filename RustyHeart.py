import sys
import random
import rusty
import pygame
import box
import Spike

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
		self.boxImages = {"metal3": pygame.image.load('images/mboxbw3.png').convert_alpha(),"metal":pygame.image.load("images/mbox1.png").convert_alpha(),"cardboard":pygame.image.load("images/cbox.png").convert_alpha()}
		self.objects = []
		self.Spikes = []

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
		if obj.rect.right > 0 or obj.rect.left <self.screensize[0]:
			self.screen.blit(obj.image,obj.rect)
			self.refresh.append(obj.rect)
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
		for item in self.objects:
			if item.rect.left <self.screensize[0] and item.rect.right >0:
				self.drawBkg(background,item.rect)
			item.move(self.objects,diffX)
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
		column = 0

		mCount = 0
		for i in level:
			for obj in i:
				if obj == '.':
					column += metalSize
					mCount = 0
				elif obj == 'm':
					self.objects.append(box.Box([column,row],"metal",self.rusty,self.boxImages))
					column +=metalSize
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
					
					self.objects.append(box.Box([column,row],"cardboard",self.rusty,self.boxImages))
					column += cardboardSize
					mCount = 0
				elif obj == 's':
					
					spike = Spike.Spike([column, row])
					self.objects.append(spike)
					self.Spikes.append(spike)
					column += 50
			mCount = 0
			column = 0
			row +=50
		self.rusty.reset()
		self.screen.blit(self.rusty.image,self.rusty.rect)
		for item in self.objects:
			self.blit(item)
		pygame.display.update()

	def main(self):
		self.refresh = []
		
		soundstate = "start"
		pygame.mixer.music.load('music/start.mp3')
		pygame.mixer.music.play(-1)
		jump = pygame.mixer.Sound( "music/jumping.wav" )
		jump.set_volume(0.05)
		pickup = pygame.mixer.Sound( "music/pickup.wav" )
		pickup.set_volume(0.05)
		drop = pygame.mixer.Sound( "music/drop.wav" )
		drop.set_volume(0.05)
		fall = pygame.mixer.Sound( "music/falling.wav" )
		fall.set_volume(0.1)
		while True:
			if soundstate == "play":
				pygame.mixer.music.play(-1)
				soundstate = "start"
			if self.state == "start":
				'''Creates the start screen'''
				soundstate == "play"
				self.drawBkg(imageName = "images/heartPicture.png")
				
				afont = pygame.font.SysFont("Arial", 72)
				title = afont.render("Rusty Heart",True,(255,255,255))
				self.screen.blit(title,(120,60))

				afont = pygame.font.SysFont("Times New Roman", 25, italic = True, bold = True)
				space = afont.render("press ENTER to play", True, (255,255,255))
				self.screen.blit(space,(190,350))
				
				instruct = afont.render("press i for instructions", True, (255,255,255))
				self.screen.blit(instruct,(175,390))

				quit = afont.render("press q to quit", True, (255,255,255))
				self.screen.blit(quit,(220,430))
				
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							sys.exit()
						if event.key == pygame.K_i:
							self.state = "instructions"
							pygame.mixer.music.load('music/AdventureMeme.mp3')
							soundstate = "play"
						if event.key == pygame.K_RETURN:
							self.state = "sandbox"
							pygame.mixer.music.load('music/chaos.mp3')
							soundstate = "play"
							self.loadLevel('levels/level1.csv','images/factory.png')

							
				pygame.display.update(self.refresh)
			
			if self.state == "sandbox":
				self.refresh = []
				for event in pygame.event.get():
					#Handles key presses
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							self.state = "end"
							pygame.mixer.music.load('music/AllThis.mp3')
							soundstate = 'play'
						if event.key == pygame.K_s:
							self.rusty.fast = True
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
								if item.type != 'spike':
									item.pickUp()
							pickup.play()
					if event.type == pygame.KEYUP:
						if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
							self.rusty.stop()
						if event.key == pygame.K_s:
							self.rusty.fast = False
						if event.key == pygame.K_SPACE:
							if self.rusty.box != None:
								self.rusty.box.drop()
								drop.play()
				
				if self.rusty.rect.centery >self.screensize[1] :
					#Go back to beginning if dead
					self.rusty.left = False
					self.rusty.speed = [0,0]
					
					fall.play()
					self.state = 'end'
					pygame.mixer.music.load('music/AllThis.mp3')
					soundstate = 'play'
					
				self.updateState('images/factory.png')

				# throttle the game speed to 30fps
				self.clock.tick(30)

				#code for the death involving spikes
				for spike in self.Spikes:
					if spike.collidesWith(self.rusty.rect):
						#Go back to beginning if dead
						self.rusty.left = False
						self.rusty.speed = [0,0]
						
						fall.play()
						self.state = 'end'
						pygame.mixer.music.load('music/AllThis.mp3')
						soundstate = 'play'
						
			if self.state == "instructions":
				'''Creates an instructions page'''
				self.drawBkg()
				afont = pygame.font.SysFont("Times New Roman", 50)
				title = afont.render("Instructions",True,(0,0,0))
				self.screen.blit(title,(200,20))
				
				arrows = pygame.image.load( "images/arrowkeys.png" ).convert_alpha()
				self.screen.blit( arrows, (10, 80) )

				space = pygame.image.load( "images/spacebar.png" ).convert_alpha()
				self.screen.blit( space, (45, 260) )
				
				rkey = pygame.image.load( "images/rkey.png" ).convert_alpha()
				self.screen.blit( rkey, (140, 360) )
				
				afont = pygame.font.SysFont("Times New Roman", 20, italic = True, bold = True)
				bounce = afont.render("press to jump",True,(0,0,0))
				self.screen.blit(bounce,(210,120))
								
				move = afont.render("press to move",True,(0,0,0))
				self.screen.blit(move,(260,180))
				
				upbox = afont.render("hold to pickup boxes",True,(0,0,0))
				self.screen.blit(upbox,(255,280))
				
				fast = afont.render("press to speed up",True,(0,0,0))
				self.screen.blit(fast,(250,360))
				
				rustyleft = pygame.image.load( "images/leftrusty.png" ).convert_alpha()
				self.screen.blit( rustyleft, (410, 85) )
				
				rustyright = pygame.image.load( "images/rightrusty.png" ).convert_alpha()
				self.screen.blit( rustyright, (490, 85) )
				
				rustybox = pygame.image.load( "images/rustybox.png" ).convert_alpha()
				self.screen.blit( rustybox, (435, 185) )
				
				space = afont.render("press ENTER to go back", True, (155,50,50))
				self.screen.blit(space,(210,430))
				
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							sys.exit()
						if event.key == pygame.K_RETURN:
							self.state = "start"
							pygame.mixer.music.load('music/start.mp3')
							soundstate = "play"
											
				pygame.display.update(self.refresh)		
			
			if self.state == "end":
				'''Creates a game over page'''
				self.drawBkg()	
				afont = pygame.font.SysFont("Times New Roman", 50)
				title = afont.render("Game Over",True,(0,0,0))
				self.screen.blit(title,(210,20))
				
				rusty = pygame.image.load( "images/rustysmall.png" ).convert_alpha()
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
							pygame.mixer.music.load('music/radiomartini.mp3')
							soundstate = "play"
						if event.key == pygame.K_RETURN:
							self.state = "start"
							pygame.mixer.music.load('music/start.mp3')
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
				#resources.append(afont.render("Start Screen Image: https://www.flickr.com/photos/seanfx/", True,(0,0,0)))
				resources.append(afont.render("Bruce: http://cs.colby.edu/maxwell/", True, (0,0,0)))
				resources.append(afont.render("Music: Kevin Macleod at http://incompetech.com/",True,(0,0,0)))
				resources.append(afont.render("Sounds: GarageBand", True, (0,0,0)))
				for i in range(len(resources)):
					self.screen.blit(resources[i],(10,resourcesLoc+110+20*i))

				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							self.state = "thanks"
							pygame.mixer.music.load('music/spazzmaticpolka.mp3')
							soundstate = "play"
				pygame.display.update(self.refresh)
				
			if self.state == "thanks":
				self.drawBkg()
				bruce = pygame.image.load( "images/Bruce-Header-Collage.png" ).convert_alpha()
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



			







