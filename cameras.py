from math import sqrt
from iancraft.constants import MOUSE
from iancraft.sprites import GameSprite
from pygame import key
from pygame import mouse
from pygame.locals import K_RIGHT
from pygame.locals import K_LEFT
from pygame.locals import K_DOWN
from pygame.locals import K_UP
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEBUTTONUP
from pygame.locals import MOUSEMOTION
from pygame.rect import Rect


class Camera(GameSprite):
    def __init__(self, x, y, lw, lh, resourcemgr):
        super(Camera, self).__init__(x, y, resourcemgr=resourcemgr)
        self.w = self.resourcemgr.sw
        self.h = self.resourcemgr.sh
        self.speed = self.resourcemgr.config.getint('general',
            'camera_speed') * self.resourcemgr.scale
        self.scroll_width = self.w * (self.resourcemgr.config.getint('general',
            'scroll_width') / 100.0)
        self.rect = Rect(x, y, self.w, self.h)
        self.level_width = lw
        self.level_height = lh
        self.x_speed = 0.0
        self.y_speed = 0.0
        self.x_first = None
        self.y_first = None
        self.x_delta = None
        self.y_delta = None

    def input(self, event):
        self.x_speed = 0.0
        self.y_speed = 0.0
        x, y = mouse.get_pos()

        if event.type == MOUSEBUTTONDOWN and event.button == MOUSE.MIDDLE:
            self.x_first = x
            self.y_first = y
        elif event.type == MOUSEBUTTONUP and event.button == MOUSE.MIDDLE:
            self.x_first = None
            self.y_first = None
        elif event.type == MOUSEMOTION and mouse.get_pressed()[1] and \
            self.x_first and self.y_first:
            self.x_delta = x - self.x_first
            self.y_delta = y - self.y_first
        else:
            if mouse.get_focused():
                if x > self.w - self.scroll_width and x < self.w:
                    self.x_speed = self.speed
                elif x < self.scroll_width:
                    self.x_speed = -self.speed
                if y > self.h - self.scroll_width:
                    self.y_speed = self.speed
                elif y < self.scroll_width:
                    self.y_speed = -self.speed

            if key.get_focused():
                if key.get_pressed()[K_RIGHT]:
                    self.x_speed = self.speed
                elif key.get_pressed()[K_LEFT]:
                    self.x_speed = -self.speed
                if key.get_pressed()[K_DOWN]:
                    self.y_speed = self.speed
                elif key.get_pressed()[K_UP]:
                    self.y_speed = -self.speed

    def logic(self, ticks):
        if self.x_delta or self.y_delta:
            if self.x_delta:
                self.x -= self.x_delta
                self.x_first += self.x_delta
            if self.y_delta:
                self.y -= self.y_delta
                self.y_first += self.y_delta
            self.x_delta = None
            self.y_delta = None
        elif self.x_speed or self.y_speed:
            x_part = self.x_speed * (ticks / 1000.0)
            y_part = self.y_speed * (ticks / 1000.0)

            if x_part and y_part:
                self.x += x_part / sqrt(2.0)
                self.y += y_part / sqrt(2.0)
            elif x_part:
                self.x += x_part
            elif y_part:
                self.y += y_part

        if self.x < 0:
            self.x = 0
        if self.x > self.level_width - self.w:
            self.x = self.level_width - self.w
        if self.y < 0:
            self.y = 0
        if self.y > self.level_height - self.h:
            self.y = self.level_height - self.h

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
