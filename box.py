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
		self.collide = False
		self.rect = self.image.get_rect().move(self.start[0],self.start[1])
	def pickUp(self):
		if(self.type=="cardboard" and self.rusty.box == None):
			if not self.rusty.isOnBox(self):
				if self.rect.centery >= self.rusty.rect.top and self.rect.centery <= self.rusty.rect.bottom and ((self.rusty.left and self.rusty.rect.right >= self.rect.right and self.rusty.rect.left <= self.rect.right) or (not self.rusty.left and self.rusty.rect.left <= self.rect.left and self.rusty.rect.right >= self.rect.left)):
					self.state = 'held'
					self.rusty.box = self
	def drop(self):
		if self.state == 'held':
			self.state = 'dropped'
		
	def isOnBox(self,boxes):
		b = False
		for box in boxes:
			if box != self and box.type!='heart':
				if self.rect.colliderect(box.rect):
					box.collide = True
				if (box.rect.bottom >= self.rect.bottom) and(box.rect.top <= self.rect.bottom) and (box.rect.right >= self.rect.centerx) and (box.rect.left <= self.rect.centerx):
					b = box

		return b
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
					self.speed[1] += 2

			elif self.state == 'dropped':
				self.state = 'ground'
				if not self.rusty.left:
					self.speed[0] = self.rusty.rect.right -self.rect.left
				else:
					self.speed[0] = self.rusty.rect.left-self.rect.right
				self.rusty.box = None
		
		self.rect.move_ip(self.speed[0]-diffX, self.speed[1])

if __name__ == '__main__':
	print "please go to RustyHeart.py to play"