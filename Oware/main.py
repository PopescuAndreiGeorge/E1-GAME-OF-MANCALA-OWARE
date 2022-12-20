import pygame
from button import Button
from constants import *
from board import Board
import random

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def get_random_possible_move(possible_moves):
    list_of_valid_events=[]
    for index,elem in enumerate(possible_moves):
        if elem == 1:
            list_of_valid_events.append(index)
    return random.choice(list_of_valid_events)


def menu():
    """This function will create the main menu with the
       options of selecting the game type."""
    menu_loop = True
    clock = pygame.time.Clock()
    board = Board()
    player = 1
    warning = ""
    while menu_loop:
        clock.tick(FPS)
        if board.screen_value == 0:  # verify if we are in the menu or the actual game screen
            pygame.display.set_caption("Menu")
            board = Board()  # every time we get in the main menu, we create a new board for the game
            player = 1
            SCREEN.fill(LIGHT_BROWN)
            mouse_pos = pygame.mouse.get_pos()
            menu_render = pygame.font.Font('freesansbold.ttf', 40).render("MENU", True, BLACK)
            menu_rect = menu_render.get_rect(center=(WIDTH / 2, 50))

            # We create the 3 buttons in the menue
            PVP_button = Button(text_string="PLAYER VS PLAYER", pos=(WIDTH / 2, HEIGHT * 0.33))
            PVAI_button = Button(text_string="PLAYER VS AI", pos=(WIDTH / 2, HEIGHT * 0.5))
            quit_button = Button(text_string="QUIT", pos=(WIDTH / 2, HEIGHT * 0.66))
            button_list = [PVP_button, PVAI_button, quit_button]

            SCREEN.blit(menu_render, menu_rect)

            for button in button_list:
                button.hover(mouse_pos)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_loop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PVP_button.verify_click(mouse_pos):
                        board.screen_value = 1
                    if PVAI_button.verify_click(mouse_pos):
                        board.screen_value = 2
                    if quit_button.verify_click(mouse_pos):
                        pygame.quit()
                        return

        else:
            SCREEN.fill(LIGHT_BROWN)
            if board.screen_value == 1:
                pygame.display.set_caption("Oware P Vs P")
            else:
                pygame.display.set_caption("Oware P Vs AI")
            mouse_pos = pygame.mouse.get_pos()
            quit_button = Button(text_string="Quit to main menu", pos=(WIDTH / 2, HEIGHT - 100))
            quit_button.hover(mouse_pos)
            quit_button.update(SCREEN)
            possible_moves = board.get_possible_moves()
            # verify if the player can make a valid move
            if not board.game_over:
                if possible_moves[0] == [0, 0, 0, 0, 0, 0] and player == 1 or possible_moves[1] == [0, 0, 0, 0, 0,
                                                                                                    0] and player == 2:
                    board.update_score_with_sum_on_row()
                    board.game_over = True
            # verify each event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_loop = False
                # if we are playing a PVP match, or we are playing VS AI, and it's the player's turn
                if board.screen_value == 1 or board.screen_value == 2 and player == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if quit_button.verify_click(mouse_pos):
                            board.screen_value = 0
                        # if the game is not over we can continue to make moves that will update the board
                        if not board.game_over:
                            row, column = board.get_clicked_pit(mouse_pos)
                            if row != -1 and column != -1:
                                if player == 1 and row == 1:
                                    warning = "Invalid row for player 1"
                                elif player == 2 and row == 0:
                                    warning = "Invalid row for player 2"
                                else:
                                    # because we verified beforehand the row being the correct one for the player,
                                    # the row for this method will serve
                                    # as the actual coordinate and as the plyer number
                                    if possible_moves[row][column] == 0:
                                        warning = "Invalid move"
                                    else:
                                        board.update_game_state(row, column)
                                        warning = ""
                                        if player == 1:
                                            player = 2
                                        else:
                                            player = 1
                # it's the AI's turn to play
                elif board.screen_value == 2 and player == 2:
                    row=1
                    column = get_random_possible_move(possible_moves[1])
                    board.update_game_state(row, column)
                    player = 1

            board.draw(SCREEN, player, warning)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    menu()
