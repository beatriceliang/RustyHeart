import pygame
class Door:
	def __init__(self,location):
		self.location = location
		self.image = pygame.image.load("images/door.png")
		self.rect = self.image.get_rect().move(location[0], location[1]-50)
		self.type = "door"
		self.collide = True
		self.active = True
	def move(self,objects,diffX):
		self.rect.move_ip(-diffX, 0)