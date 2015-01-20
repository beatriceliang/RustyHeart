import sys
import random
import pygame
class Rusty:
    def __init__(self,start):
        pygame.init()
        self.start = start
        self.speed = [0,0]
        
        self.rightImage = pygame.image.load("images/rightrusty.png").convert_alpha()
        self.leftImage = pygame.image.load("images/leftrusty.png").convert_alpha()
        self.waveImage = pygame.image.load("images/rustysmaller.png").convert_alpha()
        self.image = self.rightImage
        self.left = False
        self.rect = self.image.get_rect().move(self.start[0],self.start[1])
        self.justJumped = False
        self.box = None

        self.fast = False
    def reset(self):
        self.rect = self.image.get_rect().move(self.start[0],self.start[1])
    def speedLeft(self):
        self.image = self.leftImage
        self.left = True
        if self.fast:
            self.speed[0]=-7
        else:
            self.speed[0]=-5
    def speedRight(self):
        self.image = self.rightImage
        self.left = False
        if self.fast:
            self.speed[0]=7
        else:
            self.speed[0]=5
    def stop(self):
        self.speed[0] = 0
        
    def wave(self):
    	self.image = self.waveImage
    	self.left = False
        
    def jump(self):
        if not self.justJumped:
            self.speed[1]= -75
            self.justJumped = True
    def isOnBox(self,box):
        return (box.rect.centery +box.rect.height/2 >= self.rect.centery +self.rect.height/2) and (box.rect.centery-box.rect.height/2 <= self.rect.centery + self.rect.height/2) and (box.rect.centerx + box.rect.width/2 >= self.rect.centerx) and (box.rect.centerx-box.rect.width/2 <= self.rect.centerx)
    def move(self,boxes,diffX):
        notOn = True
        b = None
        i = 0
        for box in boxes:
            if box.type != "door" or (box.type=="heart" and box.visible==True):
                if self.rect.colliderect(box.rect):
                    box.collide = True
                    if box.type=="heart" and not box.rect.colliderect(boxes[i+1].rect):
                    	    box.visible=True
                else:
                    box.collide = False
                if box.rect.left <640 and box.rect.right>0:
                    if not self.justJumped and self.left and self.rect.colliderect(box.rect) and self.rect.left <= box.rect.right and self.rect.right >=box.rect.right and self.rect.bottom > box.rect.centery:
                        if not(box.type=="heart" and box.visible==True):
                        	self.stop()
                    elif not self.justJumped and not self.left and self.rect.colliderect(box.rect) and self.rect.right >= box.rect.left and self.rect.left <= box.rect.left and self.rect.bottom > box.rect.centery:
                        if not(box.type=="heart" and box.visible==True):
				 self.stop()
                    if box.type =="metal" and self.rect.centerx > box.rect.left and self.rect.centerx <box.rect.right and self.rect.top >= box.rect.bottom and self.rect.top < box.rect.bottom + box.rect.height:
                    	self.justJumped = False
                    	self.speed[1] = 0
                    
                    if self.isOnBox(box):
                        if box == self.box or box.type=="heart":
                            continue
                        notOn = False
                        b = box
            i+=1 

        if notOn ^ self.justJumped:
            self.speed[1] +=  2
        else:
            self.speed[1] = 0
            self.justJumped = False
        if b != None and not self.justJumped:
            self.speed[1] = b.rect.top-self.rect.height-self.rect.top
        self.rect.move_ip(self.speed[0]-diffX, self.speed[1])
 
        
