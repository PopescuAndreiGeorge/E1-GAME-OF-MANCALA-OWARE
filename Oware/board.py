import pygame
from constants import *


class Board:
    def __init__(self):
        self.board = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.screen_value = 0
        self.player1_score = 0
        self.player2_score = 0
        self.game_over = False

    def game_result(self):
        """The function verifies in which state the game is:
            0: the game is not finished
            1: it's a tie
            2: Player 1 wins
            3: Player 2 wins
        """
        if self.player1_score == 24 and self.player2_score == 24:
            return 1
        if self.player1_score >= 25:
            return 2
        elif self.player2_score >= 25:
            return 3
        return 0

    def add_text(self, pos, message, font, color, screen):
        """The function renders the table, pits and messages
        :param pos: the coordinates for the message
        :param message: the text to be printed
        :param font: the font used for the text
        :param color: the color used for the text
        :param screen: the main screen game
        """
        text = font.render(message, True, color)
        text_rect = text.get_rect()
        text_rect.center = pos
        screen.blit(text, text_rect)

    def draw(self, screen, player, warning_message):
        """The function renders the table, pits and messages
        :param screen: the main screen game
        :param player: current plyer number
        :param warning_message: a warning message created by an incorrect player action
        """
        pygame.draw.rect(screen, LIGHT_GRAY,
                         (BOARD_WIDTH // 2 - 150, BOARD_HEIGHT // 2 + 40, BOARD_WIDTH, BOARD_HEIGHT // 2 - 15))
        pygame.draw.rect(screen, BLACK,
                         (BOARD_WIDTH // 2 - 150, BOARD_HEIGHT // 2 + 40, BOARD_WIDTH, BOARD_HEIGHT // 2 - 15), 1)

        pygame.draw.rect(screen, LIGHT_GRAY,
                         (BOARD_WIDTH // 2 - 150, BOARD_HEIGHT // 2 + BOARD_HEIGHT // 2 + 35, BOARD_WIDTH,
                          BOARD_HEIGHT // 2 - 20))
        pygame.draw.rect(screen, BLACK,
                         (BOARD_WIDTH // 2 - 150, BOARD_HEIGHT // 2 + BOARD_HEIGHT // 2 + 35, BOARD_WIDTH,
                          BOARD_HEIGHT // 2 - 20), 1)

        font = pygame.font.Font('freesansbold.ttf', 34)
        result = self.game_result()
        match result:
            case 1:
                self.game_over = True
                player_render = font.render("Tie", True, BLACK)
                text_rect = player_render.get_rect()
                text_rect.center = (WIDTH / 2, 50)
                screen.blit(player_render, text_rect)
            case 2:
                self.game_over = True
                player_render = font.render("Player 1 wins", True, DARK_RED)
                text_rect = player_render.get_rect()
                text_rect.center = (WIDTH / 2, 50)
                screen.blit(player_render, text_rect)
            case 3:
                self.game_over = True
                player_render = font.render("Player 2 wins", True, CYAN)
                text_rect = player_render.get_rect()
                text_rect.center = (WIDTH / 2, 50)
                screen.blit(player_render, text_rect)
            case 0:
                match player:
                    case 1:
                        player_render = font.render("Player's 1 turn", True, DARK_RED)
                        text_rect = player_render.get_rect()
                        text_rect.center = (WIDTH / 2, 50)
                        screen.blit(player_render, text_rect)
                    case 2:
                        player_render = font.render("Player's 2 turn", True, CYAN)
                        text_rect = player_render.get_rect()
                        text_rect.center = (WIDTH / 2, 50)
                        screen.blit(player_render, text_rect)
        for row in range(2):
            for col in range(6):
                X = BOARD_WIDTH // 2 + RADIUS * col * 2.4 - 90
                Y = BOARD_HEIGHT // 2 + RADIUS * row * 3 + 95

                if row == 0:
                    circleColor = GREY_RED
                else:
                    circleColor = GREY_CYAN

                pygame.draw.circle(screen, circleColor, (X, Y), RADIUS)
                pygame.draw.circle(screen, BLACK, (X, Y), RADIUS + 1, 1)

                # rendering the number of stones in each pit
                self.add_text((X, Y), str(self.board[row][col]), pygame.font.Font('freesansbold.ttf', 32), BLACK,
                              screen)
                # rendering player1 score
                self.add_text((450, 135), "Player 1 : {0}".format(self.player1_score),
                              pygame.font.Font('freesansbold.ttf', 25), DARK_RED, screen)
                # rendering player2 score
                self.add_text((450, 415), "Player 2 : {0}".format(self.player2_score),
                              pygame.font.Font('freesansbold.ttf', 25), CYAN, screen)
                # if a wrong move was selected, we render a warning
                if warning_message:
                    self.add_text((450, 100), "Warning : {0}".format(warning_message),
                                  pygame.font.Font('freesansbold.ttf', 30), BLACK, screen)
