# Heart.py
# Luis Henriquez-Perez
# Tue Jan 20 2015
# This class if for the spike class in the game Rusty Heart

import pygame

class Heart:
    def __init__(self, location):
       self.location = location
       #self.visible = False
       self.type = 'heart'
       self.image = pygame.image.load("images/littleHeart.png")
       self.rect = self.image.get_rect().move(location[0],location[1])

    def move(self, objects, diffX):
		self.rect.move_ip(-diffX, 0)
