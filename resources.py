import os
import sys
import shutil
import pygame
from ConfigParser import RawConfigParser
from iancraft.constants import BACKGROUNDS
from iancraft.constants import BUTTONS
from iancraft.constants import TILE_SHEETS
from iancraft.constants import UNITS
from iancraft.constants import UI_SCALE_DEFAULT
from iancraft.utils import load_image
from iancraft.utils import load_sound
from iancraft.utils import logger
from pygame import display
from pygame.transform import scale


class ResourceManager(object):
    def __init__(self):
        self.init_paths()
        self.init_config()
        self.init_screen()

        self.unit_images = {}
        self.scaled_unit_images = {}
        for u in UNITS:
            self.unit_images[u] = load_image(self.main_path,
                'units/%s.png' % u, -1)

        self.tile_images = {}
        self.scaled_tile_images = {}
        for s in TILE_SHEETS:
            self.tile_images[s] = load_image(self.main_path,
                'tiles/%s.png' % s)

        self.button_images = {}
        self.scaled_button_images = {}
        for b in BUTTONS:
            self.button_images[b] = load_image(self.main_path,
                'buttons/%s.png' % b, -1)

        self.background_images = {}
        self.scaled_background_images = {}
        for b in BACKGROUNDS:
            self.background_images[b] = load_image(self.main_path,
                'backgrounds/%s.jpg' % b)

        self.unit_sounds = {}
        for u in UNITS:
            self.unit_sounds[u] = {}
            self.unit_sounds[u]['move'] = load_sound(self.main_path,
                'units/%s.move.ogg' % u)
            self.unit_sounds[u]['fire'] = load_sound(self.main_path,
                'units/%s.fire.ogg' % u)
            self.unit_sounds[u]['target'] = load_sound(self.main_path,
                'units/%s.target.ogg' % u)
            self.unit_sounds[u]['die'] = load_sound(self.main_path,
                'units/%s.die.ogg' % u)

        self.update_scale()

    def init_paths(self):
        if hasattr(sys, 'frozen') and sys.frozen in ('windows_exe',
            'console_exe', True):
            self.main_path = os.path.dirname(os.path.abspath(sys.executable))
        else:
            self.main_path = os.path.dirname(os.path.realpath(__file__))
        game_path = os.path.expanduser('~')
        if sys.platform == 'win32':
            game_path = os.path.join(game_path, 'Documents/My Games/iancraft')
        else:
            game_path = os.path.join(game_path, '.local/share/iancraft')
        self.game_path = game_path

        self.maps_path = os.path.join(game_path, 'maps')
        self.saves_path = os.path.join(game_path, 'saves')
        if not os.path.exists(self.maps_path):
            os.makedirs(self.maps_path)
        if not os.path.exists(self.saves_path):
            os.makedirs(self.saves_path)
        logger.add_file_handler(self.main_path)

    def init_config(self):
        default_cfg_path = os.path.join(self.game_path, 'default.ini')
        shutil.copy(os.path.join(self.main_path, 'default.ini'),
            default_cfg_path)
        cfg_path = os.path.join(self.game_path, 'user.ini')

        config = RawConfigParser()
        config.readfp(open(default_cfg_path))
        if os.path.exists(cfg_path):
            config.read([cfg_path])
        config.write(open(cfg_path, 'w'))  # add new defaults

        self.config = config

    def init_screen(self):
        screen_info = display.Info()
        self.desktop_width = screen_info.current_w
        self.desktop_height = screen_info.current_h

        self.get_screen_size()
        display.set_icon(load_image(self.main_path, 'iancraft.ico',
            convert=False))
        self.screen = display.set_mode((self.sw, self.sh), self.flags)
        display.set_caption('IanCraft')

    def get_screen_size(self):
        self.flags = 0  # pygame.DOUBLEBUF
        if self.config.getint('general', 'fullscreen') == 0:
            self.sw = self.config.getint('general', 'window_width')
            self.sh = self.config.getint('general', 'window_height')
            # self.flags |= pygame.OPENGL
        elif self.config.getint('general', 'fullscreen') == 1:
            self.sw = self.config.getint('general', 'fullscreen_width')
            self.sh = self.config.getint('general', 'fullscreen_height')
            self.flags |= pygame.FULLSCREEN | pygame.HWSURFACE | \
                pygame.DOUBLEBUF
        else:
            self.sw = self.desktop_width
            self.sh = self.desktop_height
            self.flags |= pygame.NOFRAME  # | pygame.OPENGL
            os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

    def update_scale(self):
        self.get_screen_size()
        self.scale = self.sh / UI_SCALE_DEFAULT
        self.rescale_images()

    def rescale_images(self):
        for u in self.unit_images:
            self.scaled_unit_images[u] = self.scale_image(self.unit_images[u])

        for t in self.tile_images:
            self.scaled_tile_images[t] = self.scale_image(self.tile_images[t])

        for b in self.button_images:
            self.scaled_button_images[b] = self.scale_image(
                self.button_images[b])

        for b in self.background_images:
            self.scaled_background_images[b] = self.scale_image(
                self.background_images[b])

    def scale_image(self, image):
        rect = image.get_rect()
        w = int(rect.w * self.scale)
        h = int(rect.h * self.scale)
        return scale(image, (w, h))

    def get_unit_image(self, unit):
        return self.scaled_unit_images[unit]

    def get_tile_image(self, tile):
        return self.scaled_tile_images[tile]

    def get_button_image(self, button):
        return self.scaled_button_images[button]

    def get_background_image(self, background):
        return scale(self.background_images[background], (self.sw, self.sh))

    def get_unit_sound(self, unit, sound):
        return self.unit_sounds[unit][sound]
