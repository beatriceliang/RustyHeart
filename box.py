import pygame
import sys
import random

class Box:
	def __init__(self,start,boxtype,rusty,boxImages):
		self.start = start
		self.speed = [0,0]

		self.state = 'ground'
		self.type = boxtype
		self.rusty = rusty
		self.image = boxImages[boxtype]
	
		self.rect = self.image.get_rect().move(self.start[0],self.start[1])
	def pickUp(self):
		if(self.type=="cardboard" and self.rusty.box == None):
			if((self.rusty.isOnBox(self)==False) and (self.rusty.rect.left<self.rect.left+self.rect.width*1.1 and self.rusty.rect.left>self.rect.left-self.rect.width*1.1) and (self.rusty.rect.bottom<self.rect.top+self.rect.height*2 and self.rusty.rect.bottom>self.rect.top-self.rect.height*2)):
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
	def move(self,boxes,diffX):
		
		if self.type == "cardboard":
			if self.state == 'held':
				self.speed[0] = self.rusty.rect.centerx-self.rect.centerx
				self.speed[1] = self.rusty.rect.top-self.rect.height-self.rect.top
			elif self.state == 'ground':
				b = self.isOnBox(boxes)
				self.speed[0] =0
				if b != False:
					self.speed[1] = b.rect.top-self.rect.bottom
				else:
					self.speed[1] += 5

			elif self.state == 'dropped':
				self.state = 'ground'
				if not self.rusty.left:
					self.speed[0] = self.rusty.rect.right -self.rect.left
				else:
					self.speed[0] = self.rusty.rect.left-self.rect.right
				self.rusty.box = None
		self.rect.move_ip(self.speed[0]-diffX, self.speed[1])


