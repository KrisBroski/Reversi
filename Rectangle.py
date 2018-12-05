import pygame

class Rectangle():
    def __init__(self, screen, left, top, width, height, color):
        self.left = left
        self.screen = screen
        self.top = top
        self.width = width
        self.height = height
        self.color = color

    def drawRect(self):
        pygame.draw.rect(self.screen, self.color, (self.left, self.top, self.width, self.height))

