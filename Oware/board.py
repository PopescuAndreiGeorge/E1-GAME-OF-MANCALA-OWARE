import pygame
from constants import *


def create_pits_coordinates():
    """The function crates the coordinates for the pits
    :rtype: list
    :return: a list of X and Y coordinates for each pit
    """
    result = []
    for row in range(2):
        for col in range(6):
            X = BOARD_WIDTH // 2 + RADIUS * col * 2.4 - 90
            Y = BOARD_HEIGHT // 2 + RADIUS * row * 3 + 95
            result.append([X, Y])
    return result


class Board:
    """The representation of an Oware board.
    Attributes:
        list board: a list containing 2 list, each representing the pits with the number of stone in each pit
        list pits_coordinates: a list containing 12 lists, each with 2 float values, the X and Y coordinates of each pit
        int screen_value: the type of screen in which we are: -> 0 for menu
                                                              -> 1 for P Vs P
                                                              -> 2 for P Vs AI
        int player1_score: first player's score
        int player2_score: second player's score
        bool game_over: False if the game is still going, 0 otherwise
    """
    def __init__(self):
        self.board = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.pits_coordinates = create_pits_coordinates()
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
        :rtype: int
        :return: 0 or 1 or 2 or 3 based on the logic said above
        """
        if self.player1_score == 24 and self.player2_score == 24:
            return 1
        if self.player1_score >= 25:
            return 2
        elif self.player2_score >= 25:
            return 3
        return 0

    def add_text(self, pos, message, text_font, color, screen):
        """The function renders the table, pits and messages
        :param tuple pos: the coordinates for the message
        :param str message: the text to be printed
        :param pygame.Font text_font: the font used for the text
        :param tuple color: the color used for the text
        :param pygame.Surface screen: the main screen game
        """
        text = text_font.render(message, True, color)
        text_rect = text.get_rect()
        text_rect.center = pos
        screen.blit(text, text_rect)

    def get_clicked_pit(self, pos):
        """The function verifies if the click was done in a pit,
        :param tuple pos: the mouse cursor coordinates
        :rtype: tuple
        :return: the row and column of the pit
        """
        row = -1
        column = -1
        for index, pit in enumerate(self.pits_coordinates):
            if abs(pit[0] - pos[0]) < RADIUS and abs(pit[1] - pos[1]) < RADIUS:
                if index < 6:
                    row = 0
                    column = index
                else:
                    row = 1
                    column = index - 6
                break
        return row, column

    def update_score_with_sum_on_row(self):
        """The function updated the score for both players by summing the stone left in each player part of the board
         if there are no more possible moves to be done"""
        for index,stones in enumerate(self.board[0]):
            self.player1_score+=stones
            self.board[0][index]=0
        for index,stones in enumerate(self.board[1]):
            self.player2_score+=stones
            self.board[1][index] = 0

    def update_game_state(self, row, column):
        """The function verifies if we are in a final state and updated self.game_over,
        otherwise it updates the board and scores
        :param int row: the row coordinate of the pit
        :param int column: the column coordinate of the pit
        """
        player = row
        stone = self.board[row][column]
        start_row=row
        start_column=column
        self.board[row][column]=0
        while stone:
            if row == 1:
                if column == 5:
                    row = (row + 1) % 2
                else:
                    column += 1
            else:
                if column == 0:
                    row = (row + 1) % 2
                else:
                    column -= 1
            # we make sure that we respect the rule:
            # The starting house is always left empty; if it contained 12 (or more) seeds,
            # it is skipped, and the twelfth seed is placed in the next house.
            if start_row!=row or start_column!=column:
                stone-=1
                self.board[row][column]+=1
        sum_stones=0
        while row != player:
            if self.board[row][column]==2 or self.board[row][column]==3:
                sum_stones += self.board[row][column]
                self.board[row][column]=0
                if row == 1:
                    if column == 0:
                        row = (row + 1) % 2
                    else:
                        column -= 1
                else:
                    if column == 5:
                        row = (row + 1) % 2
                    else:
                        column += 1
            else:
                break
        if player == 0:
            self.player1_score+=sum_stones
        else:
            self.player2_score += sum_stones

    def get_possible_moves(self):
        """The function gets the possible pits from where we can move the stones based on the rules:
        1. We can't move from a pit which has 0 stones
        2. If a player has 0 stones in his part of the table the other player
        must make a move that will let his opponent play
        :rtype: list
        :return: a list with 2 lists, each of them having 1 if a move from that pit is possible or 0 otherwise
        """
        result = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
        for i, row in enumerate(self.board):
            for j, stones in enumerate(row):
                if stones == 0:
                    result[i][j] = 0
            if row == [0, 0, 0, 0, 0, 0]:
                if i == 0:
                    for j, stones in enumerate(self.board[1]):
                        if stones < 6 - j:
                            result[1][j] = 0
                else:
                    for j, stones in enumerate(self.board[0]):
                        if stones < j + 1:
                            result[0][j] = 0
        return result

    def draw(self, screen, player, warning_message):
        """The function renders the table, pits and messages
        :param pygame.Surface screen: the main screen game
        :param int player: current plyer number
        :param str warning_message: a warning message created by an incorrect player action
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
                self.add_text((WIDTH / 2, 50), "Tie", font, BLACK, screen)
            case 2:
                self.game_over = True
                self.add_text((WIDTH / 2, 50), "Player 1 wins", font, DARK_RED, screen)
            case 3:
                self.game_over = True
                self.add_text((WIDTH / 2, 50), "Player 2 wins", font, CYAN, screen)
            case 0:
                match player:
                    case 1:
                        self.add_text((WIDTH / 2, 50), "Player's 1 turn", font, DARK_RED, screen)
                    case 2:
                        self.add_text((WIDTH / 2, 50), "Player's 2 turn", font, CYAN, screen)
        for index in range(12):
            if index < 6:
                circleColor = GREY_RED
                row = 0
                col = index
            else:
                circleColor = GREY_CYAN
                row = 1
                col = index - 6

            pygame.draw.circle(screen, circleColor, (self.pits_coordinates[index][0], self.pits_coordinates[index][1]),
                               RADIUS)
            pygame.draw.circle(screen, BLACK, (self.pits_coordinates[index][0], self.pits_coordinates[index][1]),
                               RADIUS + 1, 1)
            # rendering the number of stones in each pit
            self.add_text((self.pits_coordinates[index][0], self.pits_coordinates[index][1]), str(self.board[row][col]),
                          pygame.font.Font('freesansbold.ttf', 32), BLACK,
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
