# Heart.py
# Luis Henriquez-Perez
# Tue Jan 20 2015
# This class if for the spike class in the game Rusty Heart

import pygame

class Heart:
    def __init__(self, location, visible)
       self.location = location
       self.visible = False
       self.image = pygame.image.load("Heart.pgn")

    def setVisible(self, visOrNot):
        self.visible = True
