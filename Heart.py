'''
Itrat Akhter, Catherine Alden, Luis Henriquez-Perez, Beatrice Liang, Tiffany Lam, Shama Ramos
Heart
CS369 
January 2015
'''

import pygame

class Heart:
    def __init__(self, location):
       self.location = location
       self.visible = False
       self.type = 'heart'
       self.image = pygame.image.load("images/littleHeart.png")
       self.rect = self.image.get_rect().move(location[0],location[1])

    def move(self, objects, diffX):
		self.rect.move_ip(-diffX, 0)
if __name__ == '__main__':
	print "please go to RustyHeart.py to play"