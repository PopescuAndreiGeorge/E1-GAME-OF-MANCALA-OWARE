import pygame
from constants import *


class Button:
    def __init__(self, text_string, pos):
        self.pos = pos
        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.text_string = text_string
        self.text = self.font.render(text_string, True, BLACK)
        self.text_rect = self.text.get_rect(center=(self.pos[0], self.pos[1]))

    def update(self, screen):
        """The function draws the button created
        :param pygame.Surface screen: the main screen game
        """
        screen.blit(self.text, self.text_rect)

    def verify_click(self, position):
        """The function verifies if the mouse cursor is over the button
        :param tuple position: the mouse cursor position
        :rtype: bool
        :return: True if we are inside the button coordinates, False otherwise
        """
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top,
                                                                                                    self.text_rect.bottom):
            return True
        return False

    def hover(self, position):
        """The function verifies if the mouse cursor is over the button,
        therefore modifying its color
        :param tuple position: the mouse cursor position
        """
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top,
                                                                                                    self.text_rect.bottom):
            self.text = self.font.render(self.text_string, True, DARK_RED)
        else:
            self.text = self.font.render(self.text_string, True, BLACK)
