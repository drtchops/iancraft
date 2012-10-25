import os
# from iancraft.bar import Bar
from iancraft.constants import BLACK
from iancraft.constants import BLUE
from iancraft.constants import FONTS
from iancraft.constants import MOUSE
from iancraft.constants import STATES
from iancraft.constants import WHITE
from iancraft.cameras import Camera
from iancraft.states import State
from iancraft.tiles import TileManager
from iancraft.units import UnitManager
from iancraft.utils import load_sound
from iancraft.utils import set_next_state
from pygame import draw
from pygame import mouse
from pygame.font import SysFont
from pygame.locals import K_m
from pygame.locals import K_ESCAPE
from pygame.locals import KEYDOWN
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEMOTION
from pygame.mixer import music
from pygame.rect import Rect


class InGame(State):
    def __init__(self, resourcemgr, team, level):
        super(InGame, self).__init__(resourcemgr)
        self.tilemgr = TileManager(resourcemgr, level)
        self.unitmgr = UnitManager(resourcemgr, STATES.INGAME, team, level)
        self.lw = self.tilemgr.lw
        self.lh = self.tilemgr.lh
        self.team = team
        # self.bar = Bar(config)
        music.load(os.path.join(resourcemgr.main_path, 'sound/yyz.ogg'))
        self.camera = Camera(0, 0, self.lw, self.lh, resourcemgr)
        font = SysFont(FONTS, int(48 * resourcemgr.scale), True)
        self.win_msg = font.render('YOU WINNN!!! GGGG GGGGGGGGGGGGGGG', 1,
            WHITE)
        self.win_msg_rect = self.win_msg.get_rect(
            centerx=self.camera.rect.w / 2, centery=self.camera.rect.h / 4)
        self.lose_msg = font.render('You lost. What the fuck, man?', 1,
            BLACK)
        self.lose_msg_rect = self.win_msg.get_rect(
            centerx=self.camera.rect.w / 2, centery=self.camera.rect.h / 4)
        self.mouse_rect = Rect(0, 0, 0, 0)
        self.x_first = 0
        self.y_first = 0
        self.won = False
        self.lost = False
        self.gg = load_sound(resourcemgr.main_path, 'gg.ogg')
        self.lose = load_sound(resourcemgr.main_path, 'lose.ogg')

    def input_mouse(self, event):
        x, y = mouse.get_pos()
        x += self.camera.rect.x
        y += self.camera.rect.y

        if event.type == MOUSEMOTION and mouse.get_pressed()[0]:
            self.mouse_rect.x = min(self.x_first, x)
            self.mouse_rect.w = abs(self.x_first - x)
            self.mouse_rect.y = min(self.y_first, y)
            self.mouse_rect.h = abs(self.y_first - y)

        if event.type == MOUSEBUTTONDOWN and event.button == MOUSE.LEFT:
            self.mouse_rect.x = x
            self.mouse_rect.y = y
            self.mouse_rect.w = 0
            self.mouse_rect.h = 0
            self.x_first = x
            self.y_first = y

    def render_mouse_rect(self, camera):
        if mouse.get_pressed()[0] and (self.mouse_rect.w or self.mouse_rect.h):
            pos = Rect(self.mouse_rect.x - camera.rect.x,
                self.mouse_rect.y - camera.rect.y, self.mouse_rect.w,
                self.mouse_rect.h)
            draw.rect(self.resourcemgr.screen, BLUE, pos, 5)

    def input(self, event, next_state):
        next_state = super(InGame, self).input(event, next_state)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                next_state = set_next_state(next_state, STATES.MENU)
            elif event.key == K_m:
                if music.get_busy():
                    music.stop()
                else:
                    music.play()

        self.camera.input(event)
        self.unitmgr.input(event, self.camera, self.mouse_rect, self.tilemgr)
        self.input_mouse(event)

        return next_state

    def logic(self, clock, next_state):
        self.camera.logic(clock.get_time())
        self.unitmgr.logic(self.camera, clock.get_time(), self.tilemgr)

        if not self.won and not self.lost and self.unitmgr.num_enemies == 0:
            self.gg.play()
            self.won = True

        if not self.won and not self.lost and self.unitmgr.num_units == 0:
            self.lose.play()
            self.lost = True

        return next_state

    def render(self):
        self.resourcemgr.screen.fill(BLACK)
        self.tilemgr.render(self.camera)
        self.unitmgr.render(self.camera)
        self.unitmgr.play_sounds(self.camera)
        self.render_mouse_rect(self.camera)
        # self.bar.render()
        if self.won:
            self.resourcemgr.screen.blit(self.win_msg, self.win_msg_rect)
        if self.lost:
            self.resourcemgr.screen.blit(self.lose_msg, self.lose_msg_rect)
