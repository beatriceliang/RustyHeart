import pygame
import sys
import random


class Box:
	def __init__(self,location,boxtype,rusty,boxImages):
		self.location = location
		self.yspeed = 0

		self.state = 'ground'
		self.type = boxtype
		self.rusty = rusty
		self.image = boxImages[boxtype]
	
		self.rect = self.image.get_rect()
		
	def pickUp(self):
		if(self.type=="cardboard" and self.rusty.box == None):
			if((self.rusty.isOnBox(self)==False) and (self.rusty.location[0]<self.location[0]+self.rect.width*1.1 and self.rusty.location[0]>self.location[0]-self.rect.width*1.1) and (self.rusty.location[1]<self.location[1]+self.rect.height*2 and self.rusty.location[1]>self.location[1]-self.rect.height*2)):
				self.state = 'held'
				self.rusty.box = self
	
	def drop(self):
		if self.state == 'held':
			self.state = 'dropped'
		
	def isOnBox(self,boxes):
		for box in boxes:
			if box != self:
				if (box.rect.centery +box.rect.height/2 >= self.rect.centery +self.rect.height/2) and(box.rect.centery-box.rect.height/2 <= self.rect.centery + self.rect.height/2) and (box.rect.centerx + box.rect.width/2 >= self.rect.centerx) and (box.rect.centerx-box.rect.width/2 <= self.rect.centerx):
						return box
		return False
	def move(self,boxes):
		if self.type == "cardboard":
			if self.state == 'held':
				self.location[0] = self.rusty.rect.centerx-self.rect.width
				self.location[1] = self.rusty.location[1]-self.rect.height/2
			elif self.state == 'ground':
				self.location[0] = self.location[0]
				b = self.isOnBox(boxes)
				if b != False:
					self.yspeed = 0
					self.location[1] = b.location[1]-self.rect.height
				else:
					self.yspeed += 0.2
					self.location[1] += (self.rect.height/2)*self.yspeed

			elif self.state == 'dropped':
				self.state = 'ground'
				self.location[1] = self.location[1]#self.rusty.location[1]+self.rusty.rect.height-self.rect.height/2
				if not self.rusty.left:
					self.location[0] = self.rusty.location[0]+self.rect.width
				else:
					self.location[0] = self.rusty.location[0]-self.rusty.rect.width
				self.rusty.box = None


