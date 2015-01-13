import pygame
import sys
import random


class Box:
	def __init__(self,location,boxtype,rusty):
		self.location = location
		self.state = 'ground'
		self.type = boxtype
		self.rusty = rusty
		if self.type == "metal":
			self.image = pygame.image.load("mbox.png").convert_alpha()
		if self.type == "cardboard":
			self.image = pygame.image.load("cbox.png").convert_alpha()

		self.rect = self.image.get_rect()
	


	def pickUp(self):
		if(self.type=="cardboard"):
			#if((self.rusty.rect.centerx+self.rusty.rect.width/2<self.location[0]+self.rect.width/2 and self.rusty.location[0]>self.location[0]-self.rect.width/2)):
			self.state = 'held'
			self.rusty.box = self
				
		
	def drop(self):
		if self.state == 'held':
			self.state = 'dropped'
		

	def motion(self):
		if self.state == 'held':
			self.location[0] = self.rusty.rect.centerx
			self.location[1] = self.rusty.rect.centery-35
		elif self.state == 'ground':
			self.location[0] = self.location[0]
		elif self.state == 'dropped':
			self.state = 'ground'
			self.location[1] = self.rusty.rect.centery#+self.rusty.rect.height/2 
			if self.rusty.left:
				self.location[0] = self.rusty.location[0]+self.rect.width/2
			else:
				self.location[0] = self.rusty.location[0]+self.rusty.rect.width-self.rect.width/2
			self.rusty.box = None


