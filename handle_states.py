import os
import pygame
from iancraft.constants import BLACK
from iancraft.constants import FONTS
from iancraft.constants import STATES
from iancraft.constants import WHITE
from iancraft.menu import Menu
from iancraft.intro import Intro
from iancraft.ingame import InGame
from iancraft.editor import Editor
from pygame.font import SysFont


def change_state(next_state, resourcemgr):
    resourcemgr.screen.fill(BLACK)
    font = SysFont(FONTS, int(48 * resourcemgr.scale), True)
    text = font.render('Loading...', 1, WHITE)
    textpos = text.get_rect(centerx=resourcemgr.screen.get_width() / 2,
        centery=resourcemgr.screen.get_height() / 4)
    resourcemgr.screen.blit(text, textpos)
    pygame.display.flip()

    current_state = None
    if next_state == STATES.INTRO:
        current_state = Intro(resourcemgr)
    elif next_state == STATES.MENU:
        current_state = Menu(resourcemgr)
    elif next_state == STATES.INGAME:
        current_state = InGame(resourcemgr, 0,
            os.path.join(resourcemgr.main_path, 'scenarios/test.ics'))
    elif next_state == STATES.EDITOR:
        current_state = Editor(resourcemgr)

    return current_state
