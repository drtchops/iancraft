from iancraft.cameras import Camera
from iancraft.constants import BLACK
from iancraft.constants import FONTS
from iancraft.constants import MOUSE
from iancraft.constants import STATES
from iancraft.constants import WHITE
from iancraft.states import State
from iancraft.tiles import TileManager
from iancraft.utils import set_next_state
from pygame import mouse
from pygame.font import SysFont
from pygame.locals import K_ESCAPE
from pygame.locals import KEYDOWN
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEMOTION


class Editor(State):
    def __init__(self, resourcemgr, level=None):
        super(Editor, self).__init__(resourcemgr)
        self.tilemgr = TileManager(resourcemgr, level)
        self.lw = self.tilemgr.lw
        self.lh = self.tilemgr.lh
        self.camera = Camera(0, 0, self.lw, self.lh, resourcemgr)
        self.current_tile = 0
        self.font = SysFont(FONTS, int(48 * self.resourcemgr.scale), True)

    def set_tile(self):
        x, y = mouse.get_pos()
        x += self.camera.rect.x
        y += self.camera.rect.y

        for t in self.tilemgr.tiles:
            if t.rect.collidepoint(x, y):
                t.set_tile(self.current_tile)
                break

    def get_tile(self):
        x, y = mouse.get_pos()
        x += self.camera.rect.x
        y += self.camera.rect.y

        for t in self.tilemgr.tiles:
            if t.rect.collidepoint(x, y):
                self.current_tile = t.kind
                break

    def render_kind(self):
        text = 'Current Tile: %s' % self.tilemgr.tile_labels[self.current_tile]
        msg = self.font.render(text, 1, WHITE)
        msg_rect = msg.get_rect(
            centerx=self.resourcemgr.screen.get_rect().w / 2,
            centery=self.resourcemgr.screen.get_rect().h / 6)
        self.resourcemgr.screen.blit(msg, msg_rect)

    def input(self, event, next_state):
        next_state = super(Editor, self).input(event, next_state)

        self.camera.input(event)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.tilemgr.save_tiles('map1.map')
                next_state = set_next_state(next_state, STATES.MENU)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == MOUSE.LEFT:
                self.set_tile()
            elif event.button == MOUSE.RIGHT:
                self.get_tile()
            elif event.button == MOUSE.WHEELUP:
                self.current_tile -= 1
                if self.current_tile < 0:
                    self.current_tile = self.tilemgr.total_tile_kinds - 1
            elif event.button == MOUSE.WHEELDOWN:
                self.current_tile += 1
                if self.current_tile > self.tilemgr.total_tile_kinds - 1:
                    self.current_tile = 0
        elif event.type == MOUSEMOTION and mouse.get_pressed()[0]:
            self.set_tile()

        return next_state

    def logic(self, clock, next_state):
        self.camera.logic(clock.get_time())
        return next_state

    def render(self):
        self.resourcemgr.screen.fill(BLACK)
        self.tilemgr.render(self.camera)
        self.render_kind()
