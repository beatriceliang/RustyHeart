'''
Itrat Akhter, Catherine Alden, Luis Henriquez-Perez, Beatrice Liang, Tiffany Lam, Shama Ramos
Door
CS369 
January 2015
'''
import pygame
class Door:
	def __init__(self,location,levelStuff):
		self.location = location
		self.image = levelStuff["door"]
		self.rect = self.image.get_rect().move(location[0], location[1]-50)
		self.type = "door"
		self.collide = True
		self.active = True
	def move(self,objects,diffX):
		self.rect.move_ip(-diffX, 0)
if __name__ == '__main__':
	print "please go to RustyHeart.py to play"