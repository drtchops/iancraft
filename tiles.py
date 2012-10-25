import os
from iancraft.constants import FLAGS
from iancraft.kinds import set_tile_stats
from iancraft.sprites import GameSprite
from pygame.rect import Rect
from pygame.sprite import Group


class TileManager(object):
    def __init__(self, resourcemgr, level=None):
        self.resourcemgr = resourcemgr
        self.load_tiles(level) if level else self.load_default_tiles()
        self.image = self.resourcemgr.get_tile_image(self.sheet)

    def set_areas(self):
        self.areas = {}
        t = 0
        for c in xrange(self.tile_columns):
            for r in xrange(self.tile_rows):
                self.areas[t] = Rect(c * self.tile_width, r * self.tile_height,
                    self.tile_width, self.tile_height)
                t += 1

    def load_default_tiles(self, columns=40, rows=30, sheet=0,
        kinds=(0, 1, 2)):
        self.sheet = sheet
        set_tile_stats(self)
        self.set_areas()
        self.lw = columns * self.tile_width
        self.lh = rows * self.tile_height
        self.tiles = Group()
        self.walls = Group()
        y = 0
        t = 0
        for r in xrange(rows):
            x = 0
            for c in xrange(columns):
                tile = Tile(x, y, sheet, kinds[t % len(kinds)], self)
                self.tiles.add(tile)
                if tile.kind in self.wall_kinds:
                    tile.flags |= FLAGS.WALL
                    self.walls.add(tile)
                else:
                    tile.flags |= FLAGS.FLOOR

                x += self.tile_width
                t += 1
            y += self.tile_height

    def load_tiles(self, filename):
        try:
            self.tiles = Group()
            self.walls = Group()

            level = open(filename, 'r')
            line = level.readline().strip()
            while line != '[tiles]':
                line = level.readline().strip()

            self.sheet = int(level.readline().strip())
            set_tile_stats(self)
            self.set_areas()
            y = -self.tile_height
            line = level.readline().strip()
            while line and line != '[units]':
                x = 0
                y += self.tile_height
                for k in line.split(' '):
                    if not k.strip():
                        continue
                    tile = Tile(x, y, self.sheet, int(k), self)
                    self.tiles.add(tile)
                    if tile.kind in self.wall_kinds:
                        tile.flags |= FLAGS.WALL
                        self.walls.add(tile)
                    else:
                        tile.flags |= FLAGS.FLOOR
                    x += self.tile_width
                line = level.readline().strip()
            self.lw = x
            self.lh = y + self.tile_height
            level.close()
        except IOError:
            return self.load_default_tiles()

    def save_tiles(self, filename):
        columns = int(self.lw / self.tile_width)
        rows = int(self.lh / self.tile_height)
        level_dict = {}
        for t in self.tiles:
            column = t.rect.x / self.tile_width
            row = t.rect.y / self.tile_height
            level_dict.setdefault(row, {})[column] = str(t.kind)

        fullname = os.path.join(self.resourcemgr.maps_path, filename)
        level = open(fullname, 'w')
        level.write('[tiles]\n')
        level.write('%s\n' % self.sheet)
        for r in xrange(rows):
            l = []
            for c in xrange(columns):
                l.append(level_dict[r][c])
            level.write(' '.join(l))
            level.write('\n')
        level.close()

    def render(self, camera):
        for t in self.tiles:
            t.render(camera)


class Tile(GameSprite):
    def __init__(self, x, y, sheet, kind, mgr):
        super(Tile, self).__init__(x, y, kind)
        self.mgr = mgr
        self.resourcemgr = mgr.resourcemgr
        self.sheet = sheet
        set_tile_stats(self)
        self.rect = Rect(x, y, self.tile_width, self.tile_height)
        self.area = self.mgr.areas[self.kind]
        self.flags = FLAGS.TILE

    def set_tile(self, kind):
        self.kind = kind
        self.area = self.mgr.areas[kind]

    def render(self, camera=None):
        if not camera:
            self.resourcemgr.screen.blit(self.mgr.image, self.rect, self.area)
        elif self.rect.colliderect(camera):
            pos = Rect(self.rect.x - camera.rect.x,
                self.rect.y - camera.rect.y, self.rect.w, self.rect.h)
            self.resourcemgr.screen.blit(self.mgr.image, pos, self.area)
