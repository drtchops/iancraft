from iancraft.buttons import Button
from iancraft.constants import BACKGROUNDS
from iancraft.constants import BUTTONS
from iancraft.constants import FONTS
from iancraft.constants import STATES
from iancraft.constants import WHITE
from iancraft.states import State
from iancraft.utils import set_next_state
from pygame.font import SysFont
from pygame.locals import K_ESCAPE
from pygame.locals import KEYDOWN


class Menu(State):
    def __init__(self, resourcemgr):
        super(Menu, self).__init__(resourcemgr)
        self.bg = resourcemgr.get_background_image(BACKGROUNDS.MAIN_MENU)
        self.bg_rect = self.bg.get_rect()
        font = SysFont(FONTS, int(48 * self.resourcemgr.scale), True)
        self.msg = font.render('RTS TEST 3000XX', 1, WHITE)
        self.msg_rect = self.msg.get_rect(centerx=self.bg_rect.w / 2,
            centery=self.bg_rect.h / 6)

        self.start = Button((self.bg_rect.w - 100) / 2,
            self.bg_rect.h * (7 / 10.0), BUTTONS.START, resourcemgr)
        self.edit = Button((self.bg_rect.w - 100) / 2,
            self.bg_rect.h * (4 / 5.0), BUTTONS.EDIT, resourcemgr)

    def input(self, event, next_state):
        next_state = super(Menu, self).input(event, next_state)

        self.start.input(event)
        self.edit.input(event)
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            next_state = set_next_state(next_state, STATES.EXIT)
        elif self.start.was_hit:
            next_state = set_next_state(next_state, STATES.INGAME)
        elif self.edit.was_hit:
            next_state = set_next_state(next_state, STATES.EDITOR)

        return next_state

    def render(self):
        self.resourcemgr.screen.blit(self.bg, self.bg_rect)
        self.resourcemgr.screen.blit(self.msg, self.msg_rect)
        self.start.render()
        self.edit.render()
