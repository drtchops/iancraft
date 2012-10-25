import pygame
from iancraft.constants import MOUSE
from iancraft.constants import MOUSE_POS
from iancraft.kinds import set_button_stats
from iancraft.sprites import GameSprite
from pygame.locals import MOUSEMOTION
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEBUTTONUP
from pygame.rect import Rect


class Button(GameSprite):
    def __init__(self, x, y, kind, resourcemgr):
        super(Button, self).__init__(x, y, kind, resourcemgr)
        set_button_stats(self)
        self.rect = Rect(x, y, self.w, self.h)
        self.was_hit = False
        self.set_areas()
        self.area = self.areas[MOUSE_POS.OUT]

    def set_areas(self):
        self.areas = {}
        self.areas[MOUSE_POS.OVER] = pygame.Rect(0, 0, self.rect.w,
            self.rect.h)
        self.areas[MOUSE_POS.OUT] = pygame.Rect(self.rect.w, 0, self.rect.w,
            self.rect.h)
        self.areas[MOUSE_POS.DOWN] = pygame.Rect(0, self.rect.h, self.rect.w,
            self.rect.h)
        self.areas[MOUSE_POS.UP] = pygame.Rect(self.rect.w, self.rect.h,
            self.rect.w, self.rect.h)

    def input(self, event):
        x, y = pygame.mouse.get_pos()

        if event.type == MOUSEMOTION:
            if self.rect.collidepoint(x, y):
                self.area = self.areas[MOUSE_POS.OVER]
            else:
                self.area = self.areas[MOUSE_POS.OUT]

        if event.type == MOUSEBUTTONDOWN and \
            event.button == MOUSE.LEFT and self.rect.collidepoint(x, y):
            self.area = self.areas[MOUSE_POS.DOWN]
        if event.type == MOUSEBUTTONUP and event.button == MOUSE.LEFT \
            and self.rect.collidepoint(x, y):
            self.area = self.areas[MOUSE_POS.UP]
            self.was_hit = True

    def render(self):
        self.resourcemgr.screen.blit(self.image, self.rect, self.area)
