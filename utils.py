import logging
import os
import pygame
import sys
from math import sqrt
from iancraft.constants import STATES
from pygame.locals import RLEACCEL


class Log(object):
    def __init__(self):
        log = logging.getLogger('iancraft')
        log.setLevel(logging.DEBUG)
        self.f = logging.Formatter(
            '%(levelname)s %(asctime)s %(funcName)s %(lineno)d: %(message)s')

        h = logging.StreamHandler()
        h.setFormatter(self.f)
        h.setLevel(logging.WARNING)
        log.addHandler(h)

        self.log = log

    def add_file_handler(self, path):
        h = logging.FileHandler(os.path.join(path, 'game.log'))
        h.setFormatter(self.f)
        h.setLevel(logging.DEBUG)
        self.log.addHandler(h)

logger = Log()


def set_next_state(next_state, new_state):
    if next_state != STATES.EXIT:
        return new_state
    return next_state


def load_image(path, name, colorkey=None, convert=True):
    fullname = os.path.join(path, 'graphics', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        logger.log.exception('Cannot load image: %s' % name)
        sys.exit(1)

    if convert:
        image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_sound(path, name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer:
        return NoneSound()

    fullname = os.path.join(path, 'sound', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        logger.log.exception('Cannot load sound: %s' % name)
        sys.exit(1)
    return sound


def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_volume(rect, camera):
    width = 200
    d = distance(rect.x + (rect.w / 2), rect.y + (rect.h / 2),
        camera.rect.x + (camera.rect.w / 2), camera.rect.y + (camera.rect.h))
    d -= camera.rect.w / 2
    if d <= 0:
        return 1.0
    if d >= width:
        return 0.0
    return 1 - (d / width)


def get_screen_size(config):
    flags = 0  # pygame.DOUBLEBUF
    if config.getint('general', 'fullscreen') == 0:
        sw = config.getint('general', 'window_width')
        sh = config.getint('general', 'window_height')
        # flags |= pygame.OPENGL
    elif config.getint('general', 'fullscreen') == 1:
        sw = config.getint('general', 'fullscreen_width')
        sh = config.getint('general', 'fullscreen_height')
        flags |= pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    else:
        sw = config.getint('general', 'desktop_width')
        sh = config.getint('general', 'desktop_height')
        flags |= pygame.NOFRAME  # | pygame.OPENGL
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

    return sw, sh, flags
