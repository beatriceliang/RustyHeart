'''
Itrat Akhter, Catherine Alden, Luis Henriquez-Perez, Beatrice Liang, Tiffany Lam, Shama Ramos
RustyHeart Game
CS369 
January 2015
'''
import sys
import random
import rusty
import pygame
import box
import Spike
import Door
import Heart

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


		self.level = -1

		
		outdoor = {"music": pygame.mixer.Sound('music/songs/LifeofRiley.wav'),"background":pygame.image.load("images/outdoor/outdoor.png"),"metal":pygame.image.load("images/outdoor/stump1.png").convert_alpha(),"cardboard":pygame.image.load("images/outdoor/leaf.png").convert_alpha()}
		factory = {"music": pygame.mixer.Sound('music/songs/EveningofChaos.wav'), "background":pygame.image.load("images/factory/factory.png"),"metal":pygame.image.load("images/factory/mbox1.png").convert_alpha(),"cardboard":pygame.image.load("images/factory/cbox.png").convert_alpha()}
		forest = {"music": pygame.mixer.Sound('music/songs/Undaunted.wav'),"background":pygame.image.load("images/forest/forest.png"),"metal":pygame.image.load("images/forest/rock.png").convert_alpha(),"cardboard":pygame.image.load("images/forest/mushroom.png").convert_alpha()}
		coastline = {"music": pygame.mixer.Sound('music/songs/Carefree.wav'),"background":pygame.image.load("images/coastline/coastline.png"),"metal":pygame.image.load("images/coastline/beachrock.png").convert_alpha(),"cardboard":pygame.image.load("images/coastline/coconuts.png").convert_alpha()}
		space = {"music": pygame.mixer.Sound('music/songs/DestinyDay.wav'),"background":pygame.image.load("images/space/space.png"),"metal":pygame.image.load("images/space/spacestep.png").convert_alpha(),"cardboard":pygame.image.load("images/space/moonrock.png").convert_alpha()}
		self.levels = [factory,forest,outdoor,coastline,space]
		self.backgrounds = {"heartPicture":pygame.image.load("images/heartPicture.png").convert_alpha()}
		self.lifeImage = pygame.image.load("images/tinyHeart.png")
		self.objects = []
		self.Spikes = []
		self.Door = None
		self.heart = None

	def drawBkg(self, image = None, rect = None):
		'''Draws the background elements. If it is given a image name, then the background will be filled by the given image'''
		if image != None:
			background = image
		if rect == None:
			if image == None:
				self.screen.fill((255,255,255))
			else:
				self.screen.blit(background,(0,0))
			self.refresh.append(self.screen.get_rect())
		else:
			if image == None:
				self.screen.fill( (255, 255, 255), rect )
			else:
				self.screen.blit(background,rect,rect)
			self.refresh.append( rect )
	def blit(self,obj):
		'''blits an object onto the screen if it is within the screen width'''
		if obj.rect.right > 0 or obj.rect.left <self.screensize[0]:
			self.screen.blit(obj.image,obj.rect)
			self.refresh.append(obj.rect)
	def updateState(self):
		'''updates the locations of all of the objects on the screen'''
		background = self.levels[self.level]["background"]
		self.drawBkg(background,self.rusty.rect)
		if self.rusty.rect.right >= self.screensize[0]:
			diffX = self.rusty.rect.left
		elif self.rusty.rect.left < 0:
		 	diffX =  self.rusty.rect.width- self.screensize[0]
		else:
			diffX = 0
		#draws the background over each object if it moved or can move
		for item in self.objects:
			if(item.type=="cardboard" or diffX!=0 or item.type=="heart" or item.collide):
				if item.rect.left <self.screensize[0] and item.rect.right >0:
					if not(item.type=="heart" and item.visible==True):
						self.drawBkg(background,item.rect)
		#moves object
		for item in self.objects:
			if(item.type=="cardboard" or item.type == "door" or item.type=="heart" or diffX!=0 or item.collide):	
				item.move(self.objects,diffX)
				
		#blits object onto screen if it moved
		for item in self.objects:
			if item.rect.left <self.screensize[0] and item.rect.right >0:
				if item.type!="heart":
					self.screen.blit(item.image,item.rect)
					self.refresh.append(item.rect)
				else:
					if item.visible==False:
						self.screen.blit(item.image,item.rect)
						self.refresh.append(item.rect)
		#moves rusty
		self.rusty.move(self.objects,diffX)
		self.screen.blit(self.rusty.image,self.rusty.rect)

		pygame.display.update(self.refresh)

		self.refresh = []
	def loadLevel(self):
		'''loads a level from the file and adds all of the objects to the list to be drawn'''

		self.rusty.box = None
		#handles music for the level
		if self.level > -1:
			self.levels[self.level]["music"].stop()
		
		self.level += 1
		levelStuff = self.levels[self.level]
		levelStuff["music"].play(-1)

		lvl = 'levels/level'+str(self.level)+'.csv'

		
		metalSize = levelStuff["metal"].get_rect().width
		cardboardSize = levelStuff["cardboard"].get_rect().width
		self.drawBkg(levelStuff["background"])
		self.objects = []
		self.Spikes = []
		if(self.heart!=None):
			self.heart.visible = False

		#reads in file
		fp = open(lvl,'r')
		level = fp.read().split("\r")
		fp.close()
		row = 0
		column = 0

		mCount = 0
		
		for i in level:
			for obj in i:
				if obj == '.':
					column += metalSize
				#adds a metal box
				elif obj == 'm':
					self.objects.append(box.Box([column,row],"metal",self.rusty,levelStuff))
					column +=metalSize
				#adds a cardboard box
				elif obj == 'c':
					cbox = box.Box([column,row],"cardboard",self.rusty,levelStuff)
					self.objects.append(cbox)
					column += cardboardSize
				#adds a cardboard box with heart hidden behind it
				elif obj == 'C':
					self.heart = Heart.Heart([column+10, row+10])
					self.objects.append(self.heart)
					cbox = box.Box([column,row],"cardboard",self.rusty,levelStuff)
					self.objects.append(cbox)
					column += cardboardSize
				#adds a spike
				elif obj == 's':
					spike = Spike.Spike([column, row])
					self.objects.append(spike)
					self.Spikes.append(spike)
					column += 50
				#adds a door
				elif obj == 'd':
					self.Door = Door.Door([column,row])
					self.objects.append(self.Door)
					column += 50
					

			mCount = 0
			column = 0
			row +=50
		self.rusty.reset()
		self.screen.blit(self.rusty.image,self.rusty.rect)
		for item in self.objects:
			self.blit(item)
		pygame.display.update()
	def relevel(self):
		'''does the same thing as loadLevel, but without changing music and deleting hearts'''
		self.rusty.box = None
		
		lvl = 'levels/level'+str(self.level)+'.csv'

		levelStuff = self.levels[self.level]
		metalSize = levelStuff["metal"].get_rect().width
		cardboardSize = levelStuff["cardboard"].get_rect().width
		self.drawBkg(levelStuff["background"])
		self.objects = []
		self.Spikes = []
		if(self.heart!=None):
			self.heart.visible = False
		fp = open(lvl,'r')
		level = fp.read().split("\r")
		fp.close()
		row = 0
		column = 0

		mCount = 0
		#print level
		for i in level:
			for obj in i:
				if obj == '.':
					column += metalSize
				elif obj == 'm':
					self.objects.append(box.Box([column,row],"metal",self.rusty,levelStuff))
					column +=metalSize
				elif obj == 'c':
					cbox = box.Box([column,row],"cardboard",self.rusty,levelStuff)
					self.objects.append(cbox)
					column += cardboardSize
				elif obj == 'C':
					loc = [column+10, row+10]
					if loc not in self.rusty.collectedHearts:

						self.heart = Heart.Heart(loc)
						self.objects.append(self.heart)
					cbox = box.Box([column,row],"cardboard",self.rusty,levelStuff)
					self.objects.append(cbox)
					column += cardboardSize
				elif obj == 's':
					
					spike = Spike.Spike([column, row])
					self.objects.append(spike)
					self.Spikes.append(spike)
					column += 50
				elif obj == 'd':
					self.Door = Door.Door([column,row])
					self.objects.append(self.Door)
					column += 50
					

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

		#music

		startMusic = pygame.mixer.Sound('music/songs/CalltoAdventure.wav')
		instructionsMusic = pygame.mixer.Sound('music/songs/AdventureMeme.wav')

		creditsMusic = pygame.mixer.Sound('music/songs/RadioMartini.wav')
		bruceMusic = pygame.mixer.Sound('music/songs/TakeaChance.wav')
		gameOverMusic = pygame.mixer.Sound('music/songs/AllThis.wav')
		
		#sounds
		jump = pygame.mixer.Sound( "music/sounds/jumping.wav" )
		jump.set_volume(0.05)
		pickup = pygame.mixer.Sound( "music/sounds/pickup.wav" )
		pickup.set_volume(0.05)
		drop = pygame.mixer.Sound( "music/sounds/drop.wav" )
		drop.set_volume(0.05)
		fall = pygame.mixer.Sound( "music/sounds/falling.wav" )
		fall.set_volume(0.1)
		spikes = pygame.mixer.Sound( "music/sounds/spikes.wav" )
		spikes.set_volume(0.05)
		level = pygame.mixer.Sound( "music/sounds/level.wav" )
		level.set_volume(0.1)
		wave = pygame.mixer.Sound( "music/sounds/wave.wav" )

		
		startMusic.play(-1)
		while True:
			if self.state == "start":
				'''Creates the start screen'''
				self.drawBkg(image = self.backgrounds["heartPicture"])
				
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
							startMusic.stop()
							instructionsMusic.play(-1)
						if event.key == pygame.K_RETURN:
							self.state = "play"
							startMusic.stop()
							self.loadLevel()

				pygame.display.update(self.refresh)
			
			if self.state == "play":

				for i in range(self.rusty.lives):
					rect = pygame.Rect(20*i+10,10,20,17)
					self.screen.blit(self.lifeImage, rect)

				for event in pygame.event.get():
					#Handles key presses
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							self.rusty.lives = 3
							self.rusty.box = None
							self.state = "end"
							gameOverMusic.play(-1)

							self.levels[self.level]["music"].stop()

						if event.key == pygame.K_r:
							self.rusty.fast = True
						if event.key == pygame.K_LEFT:
							self.rusty.speedLeft()
						if event.key == pygame.K_RIGHT:
							self.rusty.speedRight()
						if event.key == pygame.K_DOWN:
							self.rusty.wave()	
							wave.play()
						if event.key == pygame.K_UP:
							if self.Door != None and self.Door.active and self.rusty.rect.centerx <= self.Door.rect.right and self.rusty.rect.centerx >= self.Door.rect.left and self.rusty.rect.centery >= self.Door.rect.top and self.rusty.rect.centery <= self.Door.rect.bottom:
								self.Door = None
								self.rusty.box = None
								if self.level >= len(self.levels)-1:
									self.state= "end"
									self.levels[self.level]["music"].stop()
									self.level = -1
									gameOverMusic.play(-1)

								else:
									self.loadLevel()
									level.play()

							else:
								self.rusty.jump()
								jump.play()
						if event.key == pygame.K_SPACE:

							pygame.display.update(self.refresh)
							if self.rusty.box == None:
								for item in self.objects :
									if item.type == 'cardboard':
										item.pickUp()
								pickup.play()
							else:
								self.rusty.box.drop()
						 		drop.play()
						if event.key == pygame.K_n:
							self.loadLevel()
							level.play()
					if event.type == pygame.KEYUP:
						if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
							self.rusty.stop()
						if event.key == pygame.K_r:
							self.rusty.fast = False
						
				#handles rusty dying
				for spike in self.Spikes:
					if spike.collidesWith(self.rusty.rect):
						spikes.play()
						self.rusty.lives -= 1
						self.relevel()
						
						break	
				if self.rusty.rect.centery >self.screensize[1]:
					fall.play()
					self.rusty.lives -= 1
					self.relevel()


				if self.rusty.lives <= 0:
					#Go back to beginning if dead
					self.rusty.left = False
					self.rusty.speed = [0,0]
					self.rusty.box = None
					

					self.state = 'end'

					self.levels[self.level]["music"].stop()
					self.level = -1
					gameOverMusic.play(-1)

					self.rusty.lives = 3
				
				self.updateState()
				# throttle the game speed to 30fps
				self.clock.tick(30)
						
			if self.state == "instructions":
				'''Creates an instructions page'''
				self.drawBkg()
				afont = pygame.font.SysFont("Times New Roman", 50)
				title = afont.render("Instructions",True,(0,0,0))
				self.screen.blit(title,(200,20))
				
				arrows = pygame.image.load( "images/arrowkeys.png" ).convert_alpha()
				self.screen.blit( arrows, (75, 110) )

				space = pygame.image.load( "images/spacebar.png" ).convert_alpha()
				self.screen.blit( space, (60, 270) )
				
				rkey = pygame.image.load( "images/rkey.png" ).convert_alpha()
				self.screen.blit( rkey, (120, 350) )
				
				afont = pygame.font.SysFont("Times New Roman", 20, italic = True, bold = True)
				bounce = afont.render("press to jump",True,(0,0,0))
				self.screen.blit(bounce,(200,105))
								
				move = afont.render("press to move",True,(0,0,0))
				self.screen.blit(move,(240,150))
				
				upbox = afont.render("press to pickup/drop boxes",True,(0,0,0))
				self.screen.blit(upbox,(255,270))
				
				fast = afont.render("press to run",True,(0,0,0))
				self.screen.blit(fast,(250,360))
				
				rustyleft = pygame.image.load( "images/rusty/leftrusty.png" ).convert_alpha()
				self.screen.blit( rustyleft, (410, 85) )
				
				rustyright = pygame.image.load( "images/rusty/rightrusty.png" ).convert_alpha()
				self.screen.blit( rustyright, (490, 85) )
				
				rustybox = pygame.image.load( "images/rusty/rustybox.png" ).convert_alpha()
				self.screen.blit( rustybox, (480, 185) )
				
				prevpg = afont.render("press left to go back", True, (155,50,50))
				self.screen.blit(prevpg,(50,430))
				
				nextpg = afont.render("press right for next page", True, (155,50,50))
				self.screen.blit(nextpg,(390,430))
				
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							sys.exit()
						if event.key == pygame.K_LEFT:
							self.state = "start"
							instructionsMusic.stop()
							startMusic.play(-1)
						if event.key == pygame.K_RIGHT:
							self.state = "instructions2"
												
				pygame.display.update(self.refresh)	
				
			if self.state == "instructions2":
				'''Creates the second instructions page'''
				self.drawBkg()
				afont = pygame.font.SysFont("Times New Roman", 50)
				title = afont.render("Instructions",True,(0,0,0))
				self.screen.blit(title,(200,20))
				
				spikes = pygame.image.load( "images/spike.png" ).convert_alpha()
				self.screen.blit( spikes, (100, 100) )
				
				heart = pygame.image.load( "images/littleheart.png" ).convert_alpha()
				self.screen.blit( heart, (105, 250) )
				self.screen.blit( heart, (480, 250) )
				
				door = pygame.image.load( "images/littledoor.png" ).convert_alpha()
				self.screen.blit( door, (105, 320) )
				
				afont = pygame.font.SysFont("Times New Roman", 20, italic = True, bold = True)
				spikes = afont.render("avoid hitting the spikes",True,(0,0,0))
				self.screen.blit(spikes,(220,120))
				
				heart = afont.render("collect the hearts",True,(0,0,0))
				self.screen.blit(heart,(240,270))
				
				door = afont.render("press up to walk through",True,(0,0,0))
				self.screen.blit(door,(210,345))
				
				rustyspike = pygame.image.load( "images/rusty/rustyspike.png" ).convert_alpha()
				self.screen.blit( rustyspike, (460, 40) )
				
				door = pygame.image.load( "images/rusty/rustydoor.png" ).convert_alpha()
				self.screen.blit( door, (460, 300) )				
				
				prevpg = afont.render("press left to go back", True, (155,50,50))
				self.screen.blit(prevpg,(50,430))
				
				nextpg = afont.render("press right to play", True, (155,50,50))
				self.screen.blit(nextpg,(440,430))
				
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							sys.exit()
						if event.key == pygame.K_LEFT:
							self.state = "instructions"
						if event.key == pygame.K_RIGHT:
							self.state = "start"
							instructionsMusic.stop()
							startMusic.play(-1)
												
				pygame.display.update(self.refresh)										
			
			if self.state == "end":
				'''Creates a game over page'''
				self.level = -1
				self.drawBkg()	
				afont = pygame.font.SysFont("Times New Roman", 50)
				title = afont.render("Game Over",True,(0,0,0))
				self.screen.blit(title,(210,20))
				
				rusty = pygame.image.load( "images/rusty/rustysmall.png" ).convert_alpha()
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
							gameOverMusic.stop()
							creditsMusic.play(-1)
						if event.key == pygame.K_RETURN:
							self.state = "start"
							gameOverMusic.stop()
							startMusic.play(-1)
											
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
							creditsMusic.stop()
							bruceMusic.play(-1)
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



			







