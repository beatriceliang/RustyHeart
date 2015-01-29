'''
Itrat Akhter, Catherine Alden, Luis Henriquez-Perez, Beatrice Liang, Tiffany Lam, Shama Ramos
RustyHeart
CS369 
January 2015
'''
import pygame

class Spike:
	def __init__(self, location):
		self.location = location
		self.image = pygame.image.load("images/spike.png")
		self.rect = self.image.get_rect().move(location[0], location[1])
		self.type = 'spike'
		self.collide = False
	def collidesWith(self,rusty):
		return self.rect.colliderect(rusty)
	def move(self, objects, diffX):
		self.rect.move_ip(-diffX, 0)
if __name__ == '__main__':
	print "please go to RustyHeart.py to play"