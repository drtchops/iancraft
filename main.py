#!/usr/bin/env python


if __name__ == '__main__':
    # import iancraft.<module> looks so much nicer
    import sys
    import os
    if hasattr(sys, 'frozen') and sys.frozen in ('windows_exe', 'console_exe',
        True):
        parent_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        parent_path = os.path.dirname(os.path.dirname(
            os.path.realpath(__file__)))
    sys.path.insert(0, parent_path)
    if sys.platform == 'win32':
        import pygame._view  # hack for pygame2exe in windows


import pygame
from iancraft.constants import FONTS
from iancraft.constants import STATES
from iancraft.constants import YELLOW
from iancraft.intro import Intro
from iancraft.resources import ResourceManager
from iancraft.handle_states import change_state
from iancraft.utils import logger


def init():
    pygame.mixer.pre_init(22050, -16, 50, 1024)
    pygame.init()
    pygame.mixer.set_num_channels(50)

    return ResourceManager()


def main():
    resourcemgr = init()
    clock = pygame.time.Clock()
    current_state = Intro(resourcemgr)
    next_state = STATES.NULL

    fps_timer = None
    fps_font = None
    if resourcemgr.config.getboolean('general', 'show_fps'):
        fps_timer = 0
        fps_font = pygame.font.SysFont(FONTS,
            int(48 * resourcemgr.scale), True)
        fps_interval = resourcemgr.config.getint('general', 'fps_interval')

    while next_state != STATES.EXIT:
        clock.tick(60)

        for event in pygame.event.get():
            next_state = current_state.input(event, next_state)

        next_state = current_state.logic(clock, next_state)

        if next_state not in (STATES.NULL, STATES.EXIT):
            current_state = change_state(next_state, resourcemgr)
            next_state = STATES.NULL

        current_state.render()
        if fps_timer is not None:
            if fps_timer == 0 or pygame.time.get_ticks() - fps_timer >= \
                fps_interval:
                fps_timer = pygame.time.get_ticks()
                fps = int(round(clock.get_fps()))
                fps_msg = fps_font.render(str(fps), 1, YELLOW)
                fps_rect = fps_msg.get_rect(x=resourcemgr.sw / 20,
                    y=resourcemgr.sh / 20)
            resourcemgr.screen.blit(fps_msg, fps_rect)

        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.log.exception('critical failure:')
    finally:
        pygame.quit()
