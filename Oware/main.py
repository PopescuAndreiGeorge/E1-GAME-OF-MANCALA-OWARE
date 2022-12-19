import pygame
from button import Button
from constants import *
from board import Board

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def menu():
    """This function will create the main menu with the
       options of selecting the game type."""
    menu_loop = True
    clock = pygame.time.Clock()
    board=Board()
    player = 1
    error_message = ""
    while menu_loop:
        clock.tick(FPS)
        if board.screen_value==0:  # verify if we are in the menu or the actual game screen
            pygame.display.set_caption("Menu")
            board=Board()  # every time we get in the main menu, we create a new board for the game
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
            if board.screen_value==1:
                pygame.display.set_caption("Oware P Vs P")
            else:
                pygame.display.set_caption("Oware P Vs AI")

            mouse_pos = pygame.mouse.get_pos()
            quit_button = Button(text_string="Quit to main menu", pos=(WIDTH / 2, HEIGHT - 100))
            quit_button.hover(mouse_pos)
            quit_button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_loop=False
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.verify_click(mouse_pos):
                        board.screen_value = 0

            board.draw(SCREEN, player, error_message)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    menu()
