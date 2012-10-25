from iancraft.constants import GREY
from iancraft.minimap import Minimap
from pygame import draw
from pygame.rect import Rect


class Bar(object):
    def __init__(self, config):
        sw = config.getint('general', 'screen_width')
        sh = config.getint('general', 'screen_height')
        self.w = 250
        self.h = sh
        self.rect = Rect(sw - self.w, 0, self.w, self.h)
        self.minimap = Minimap()
        self.buttons = None

    def input(self):
        pass

    def logic(self):
        pass

    def render(self, screen):
        draw.rect(screen, GREY, self.rect, 0)
