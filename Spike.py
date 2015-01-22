# Spike.py
# Luis Henriquez-Perez
# Fri Jan 16 2015
# This program represents a spike in the game Rusty Heart
import pygame

class Spike:
	def __init__(self, location):
		self.location = location
		self.image = pygame.image.load("images/spike.png")
		self.rect = self.image.get_rect().move(location[0], location[1])
		self.type = 'spike'
	def collidesWith(self,rusty):
		return self.rect.colliderect(rusty)
	def move(self, objects, diffX):
		self.rect.move_ip(-diffX, 0)