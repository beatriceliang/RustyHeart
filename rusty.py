import sys
import random
import pygame
class Rusty:
    def __init__(self,location):
        pygame.init()
        self.start = (location[0],location[1])
        self.location = location #[50,280]
        self.speed = [0,0]
        
        self.rightImage = pygame.image.load("rightrusty.png").convert_alpha()
        self.leftImage = pygame.image.load("leftrusty.png").convert_alpha()
        self.image = self.rightImage
        self.left = False
        self.rect = self.image.get_rect()
        
        self.justJumped = False
        self.box = None
    def speedLeft(self):
        self.image = self.leftImage
        self.left = True
        self.speed[0]=-0.5
    def speedRight(self):
        self.image = self.rightImage
        self.left = False
        self.speed[0]=0.5
    def stop(self):
        self.speed[0] = 0
    def jump(self):
        if not self.justJumped:
            self.speed[1]= -2
            self.justJumped = True
    def isOnBox(self,box):
        return (box.rect.centery +box.rect.height/2 >= self.rect.centery +self.rect.height/2) and (box.rect.centery-box.rect.height/2 <= self.rect.centery + self.rect.height/2) and (box.rect.centerx + box.rect.width/2 >= self.rect.centerx) and (box.rect.centerx-box.rect.width/2 <= self.rect.centerx)
    def move(self,boxes):
        notOn = True
        b = None
        for box in boxes:
            if not self.justJumped and self.left and self.rect.colliderect(box.rect) and self.rect.left <= box.rect.right and self.rect.right >=box.rect.right and self.rect.bottom > box.rect.centery:
                self.stop()
            elif not self.justJumped and not self.left and self.rect.colliderect(box.rect) and self.rect.right >= box.rect.left and self.rect.left <= box.rect.left and self.rect.bottom > box.rect.centery:
                self.stop()
            if self.isOnBox(box):
                if box == self.box:
                    continue
                notOn = False
                b = box

        if notOn ^ self.justJumped:
            self.speed[1] += 0.2
        else:
            self.speed[1] = 0
            self.justJumped = False
        
       
        tempy = self.location[1]
        self.location[0]+=(self.rect.width/2)*self.speed[0]
        
        self.location[1]+=(self.rect.height/2)*self.speed[1]
        if b != None and not self.justJumped:
            self.location[1] = b.rect.top-self.rect.height*1.5
        
        
        
