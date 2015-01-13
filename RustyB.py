import sys
import random
import pygame
class Rusty:
    def __init__(self):
        pygame.init()
        self.location = [50,320]
        self.speed = [0,0]

        self.image = pygame.image.load("rusty.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        self.justJumped = False

    def move(self):
        tempy = self.location[1]
        self.location[0]+=(self.rect.width/2)*self.speed[0]
        
        self.location[1]+=(self.rect.height/2)*self.speed[1]
        
    def speedLeft(self):
        #if not self.nextToBox():
    	self.speed[0]-=0.5
    def speedRight(self):
    	self.speed[0]+=0.5
    def jump(self):
        if(self.speed[1]> -1.0):
            self.speed[1]= -1.0
        self.justJumped = True
    def isOnBox(self,box):
        return (box.rect.centery-box.rect.height/2 <= self.rect.centery + self.rect.height/2) and (box.rect.centerx + box.rect.width/2 >= self.rect.centerx) and (box.rect.centerx-box.rect.width/2 <= self.rect.centerx)
    # def nextToBox(self,box):
    #     return (box.rect.centery+box.rect.height/2 == self.rect.centery + self.rect.height/2) and ((box.rect.centerx +box.rect.width/2 == self.rect.centerx-self.rect.width/2)
    def actions(self,boxes):
        for box in boxes:
            if not self.isOnBox(box):
                self.speed[1] += 0.5
                self.justJumped = False
            else:
                if not self.justJumped:
                    self.speed[1] = 0
             
        self.move()     
        
        
        
