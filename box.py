import pygame
import sys
import random


class Box:
	def __init__(self,location,picked,typeof):
		self.location = location
		self.picked = picked
		self.typeof = typeof
		self.image = pygame.image.load("box.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.originlocation = []
		self.originlocation.append(location[0])
		self.originlocation.append(location[1])
	def canBePicked(self,rus):
		if(self.typeof=="cardboard"):
			if((rus.location[0]<self.location[0]+self.rect.width/2 and rus.location[0]>self.location[0]-self.rect.width/2)):
				self.picked = "pickedup"
		
	def canBeDropped(self):
		if(self.typeof=="cardboard"):
			self.picked = "dropped"
	def pickup(self,rus):
		if(self.typeof=="cardboard"):
			self.location[0] = rus.location[0]
			self.location[1] = rus.location[1]
			
		
	def drop(self,rus):
		if(rus.state=="ground"):
			self.location[1] = self.location[1]
		else:
			self.location[1] = self.originlocation[1]
		self.picked = "ground"
	def stayOnGround(self):
		self.location[0] = self.location[0]
		self.location[1] = self.location[1]
		
	def pickupmotion(self,rus):
		if(self.picked=="ground"):
			self.stayOnGround()
		if(self.picked=="pickedup"):
			self.pickup(rus)
		if(self.picked=="dropped"):
			self.drop(rus)
			

