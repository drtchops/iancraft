from iancraft.constants import BACKGROUNDS
from iancraft.constants import FONTS
from iancraft.constants import STATES
from iancraft.constants import RED
from iancraft.states import State
from iancraft.utils import set_next_state
from pygame.font import SysFont
from pygame.locals import K_ESCAPE
from pygame.locals import KEYDOWN
from pygame.locals import MOUSEBUTTONUP


class Intro(State):
    def __init__(self, resourcemgr):
        super(Intro, self).__init__(resourcemgr)
        self.bg = resourcemgr.get_background_image(BACKGROUNDS.INTRO)
        self.bg_rect = self.bg.get_rect()
        font = SysFont(FONTS, int(52 * self.resourcemgr.scale), True)
        self.msg = font.render('Sprayed Studios Presents...', 1, RED)
        self.msg_rect = self.msg.get_rect(centerx=self.bg_rect.w / 2,
            centery=self.bg_rect.h / 10)

    def input(self, event, next_state):
        next_state = super(Intro, self).input(event, next_state)

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            next_state = set_next_state(next_state, STATES.EXIT)
        elif event.type == MOUSEBUTTONUP or (event.type == \
            KEYDOWN and event.key != K_ESCAPE):
            next_state = set_next_state(next_state, STATES.MENU)

        return next_state

    def render(self):
        self.resourcemgr.screen.blit(self.bg, self.bg_rect)
        self.resourcemgr.screen.blit(self.msg, self.msg_rect)
