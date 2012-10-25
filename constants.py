class Enum(type):
    def __contains__(self, val):
        return val in self.__dict__

    def __iter__(self):
        for attr in self.__dict__:
            if not attr.startswith('__'):
                yield self.__dict__[attr]

    def __len__(self):
        return len(self.names())

    def __str__(self):
        return str(self.names())

    def names(self):
        return [attr for attr in self.__dict__ if not attr.startswith('__')]

    def name(self, val):
        for attr in self.__dict__:
            if not attr.startswith('__') and val == self.__dict__[attr]:
                return attr


def enum(*sequential, **named):
    if len(sequential) == 0 and len(named) == 0:
        raise ValueError('Empty enum')
    if len(named) > 0 and (len(sequential) > min(named.values()) or
        len(set(named.values())) != len(named.values())):
        raise ValueError('Overlapping enum values')
    if len(list(sequential) + named.keys()) > len(
        set(list(sequential) + named.keys())):
        raise ValueError('Duplicate enum names')

    enums = dict(zip(sequential, range(len(sequential))), **named)
    return Enum('Enum', (), enums)


# draw everything sized as if you had a 1920x1080 resolution
UI_SCALE_DEFAULT = 1080.0
SCALABLE_VALUES = ('w', 'h', 'speed', 'range', 'tile_width', 'tile_height')

FONTS = 'monospace'

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
YELLOW = (255, 255, 0, 255)
GREY = (190, 190, 190, 255)


STATES = enum(
    'NULL',
    'INTRO',
    'MENU',
    'INGAME',
    'EDITOR',
    'CREDITS',
    'OPTIONS',
    'EXIT',
)


TEAMS = enum(
    'NAZIS',
    'GREEKS',
    'ALIENS',
)


UNITS = enum(
    'GUNNER',
    'BARRACKS',

    'ARCHER',
    'ARCHERY_RANGE',

    'SLIMER',
    'PIT',
)


MOUSE_POS = enum(
    'OVER',
    'OUT',
    'DOWN',
    'UP',
)


SELECT = enum(
    'NORM',
    'MOVING',
    'FIRING',
    'DUNNO',
)


TILE_SHEETS = enum(
    'DEFAULT',
    'RGB',
)


DEFAULT_TILES = enum(
    'RED',
    'GREEN',
    'BLUE',
    'TOPLEFT',
    'LEFT',
    'BOTTOMLEFT',
    'TOP',
    'CENTRE',
    'BOTTOM',
    'TOPRIGHT',
    'RIGHT',
    'BOTTOMRIGHT',
)


BUTTONS = enum(
    'START',
    'EDIT',
)


BACKGROUNDS = enum(
    'INTRO',
    'MAIN_MENU',
)


MOUSE = enum(
    LEFT=1,
    MIDDLE=2,
    RIGHT=3,
    WHEELUP=4,
    WHEELDOWN=5,
)


FLAGS = enum(
    UNIT=2 ** 0,
    DUDE=2 ** 1,
    STRUCT=2 ** 2,
    CAN_MOVE=2 ** 3,
    CAN_FIRE=2 ** 4,
    CAN_BUILD=2 ** 5,
    TILE=2 ** 6,
    FLOOR=2 ** 7,
    WALL=2 ** 8,
)
