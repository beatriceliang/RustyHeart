# Spike.py
# Luis Henriquez-Perez
# Fri Jan 16 2015
# This program represents a spike in the game Rusty Heart
import pygame

class Spike:
    def __init__(self, location):
        self.location = location
        self.image = pygame.image.load("Spike.py")
        self.rect = self.image.get_rect().move(location[0], location[1])
    def collidesRusty(self, Rusty):
        return self.rect.colliderect(Rusty)
