import sys
import random
import pygame
class Rusty:
    def __init__(self,start):
        pygame.init()
        self.start = start
        self.speed = [0,0]
        
        self.rightImage = pygame.image.load("rightrustybw.png").convert_alpha()
        self.leftImage = pygame.image.load("leftrustybw.png").convert_alpha()
        self.image = self.rightImage
        self.left = False
        self.rect = self.image.get_rect().move(self.start[0],self.start[1])
        self.justJumped = False
        self.box = None
    def speedLeft(self):
        self.image = self.leftImage
        self.left = True
        self.speed[0]=-10
    def reset(self):
        self.rect = self.image.get_rect().move(self.start[0],self.start[1])
    def speedRight(self):
        self.image = self.rightImage
        self.left = False
        self.speed[0]=10
    def stop(self):
        self.speed[0] = 0
    def jump(self):
        if not self.justJumped:
            self.speed[1]= -75
            self.justJumped = True
    def isOnBox(self,box):
        return (box.rect.centery +box.rect.height/2 >= self.rect.centery +self.rect.height/2) and (box.rect.centery-box.rect.height/2 <= self.rect.centery + self.rect.height/2) and (box.rect.centerx + box.rect.width/2 >= self.rect.centerx) and (box.rect.centerx-box.rect.width/2 <= self.rect.centerx)
    def move(self,boxes,diffX):
        notOn = True
        b = None
        for box in boxes:
            if box.rect.left <640 and box.rect.right>0:
                if not self.justJumped and self.left and self.rect.colliderect(box.rect) and self.rect.left <= box.rect.right and self.rect.right >=box.rect.right and self.rect.bottom > box.rect.centery:
                    self.stop()
                elif not self.justJumped and not self.left and self.rect.colliderect(box.rect) and self.rect.right >= box.rect.left and self.rect.left <= box.rect.left and self.rect.bottom > box.rect.centery:
                    self.stop()
                if box.type =="metal" and self.rect.centerx > box.rect.left and self.rect.centerx <box.rect.right and self.rect.top >= box.rect.bottom and self.rect.top < box.rect.bottom + box.rect.height:
                	self.justJumped = False
                	self.speed[1] = 0
                
                if self.isOnBox(box):
                    if box == self.box:
                        continue
                    notOn = False
                    b = box

        if notOn ^ self.justJumped:
            self.speed[1] +=  5
        else:
            self.speed[1] = 0
            self.justJumped = False
        
        if b != None and not self.justJumped:
            self.speed[1] = b.rect.top-self.rect.height-self.rect.top
        self.rect.move_ip(self.speed[0]-diffX, self.speed[1])
 
        
