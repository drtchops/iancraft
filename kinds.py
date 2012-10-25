from iancraft.constants import BUTTONS
from iancraft.constants import UNITS
from iancraft.constants import FLAGS
from iancraft.constants import TILE_SHEETS
from iancraft.constants import DEFAULT_TILES
from iancraft.constants import SCALABLE_VALUES


BUTTON_STATS = {
    BUTTONS.START: {
        'w': 100,
        'h': 60,
    },
    BUTTONS.EDIT: {
        'w': 100,
        'h': 60,
    },
}


UNIT_STATS = {
    UNITS.GUNNER: {
        'w': 50,
        'h': 50,
        'speed': 300,
        'range': 200,
        'attack_delay': 800,
        'shoot_delay': 300,
        'max_health': 100,
        'cost': 100,
        'atk': 20,
        'def': 10,
        'flags': FLAGS.UNIT | FLAGS.DUDE | FLAGS.CAN_MOVE | FLAGS.CAN_FIRE,
    },
    UNITS.BARRACKS: {
        'w': 100,
        'h': 100,
        'max_health': 2000,
        'def': 100,
        'flags': FLAGS.UNIT | FLAGS.STRUCT | FLAGS.CAN_BUILD,
        'buildables': (UNITS.GUNNER,),
    },
    UNITS.ARCHER: {
        'w': 50,
        'h': 50,
        'speed': 400,
        'range': 250,
        'attack_delay': 700,
        'shoot_delay': 200,
        'max_health': 80,
        'cost': 80,
        'atk': 15,
        'def': 10,
        'flags': FLAGS.UNIT | FLAGS.DUDE | FLAGS.CAN_MOVE | FLAGS.CAN_FIRE,
    },
    UNITS.ARCHERY_RANGE: {
        'w': 100,
        'h': 100,
        'max_health': 1500,
        'def': 80,
        'flags': FLAGS.UNIT | FLAGS.STRUCT | FLAGS.CAN_BUILD,
        'buildables': (UNITS.ARCHER,),
    },
    UNITS.SLIMER: {
        'w': 50,
        'h': 50,
        'speed': 300,
        'range': 200,
        'attack_delay': 800,
        'shoot_delay': 300,
        'max_health': 100,
        'atk': 20,
        'def': 10,
        'flags': FLAGS.UNIT | FLAGS.DUDE | FLAGS.CAN_MOVE | FLAGS.CAN_FIRE,
    },
    UNITS.PIT: {
        'w': 100,
        'h': 100,
        'max_health': 2000,
        'def': 100,
        'flags': FLAGS.UNIT | FLAGS.STRUCT | FLAGS.CAN_BUILD,
        'buildables': (UNITS.SLIMER,),
    },
}


TILE_STATS = {
    TILE_SHEETS.DEFAULT: {
        'tile_width': 80,
        'tile_height': 80,
        'tile_columns': 4,
        'tile_rows': 3,
        'total_tile_kinds': 12,
        'tile_kinds': DEFAULT_TILES,
        'wall_kinds': (
            DEFAULT_TILES.TOPLEFT,
            DEFAULT_TILES.TOP,
            DEFAULT_TILES.TOPRIGHT,
            DEFAULT_TILES.LEFT,
            DEFAULT_TILES.CENTRE,
            DEFAULT_TILES.RIGHT,
            DEFAULT_TILES.BOTTOMLEFT,
            DEFAULT_TILES.BOTTOM,
            DEFAULT_TILES.BOTTOMRIGHT,
        ),
        'tile_labels': (
            'Red Floor',
            'Green Floor',
            'Blue Floor',
            'Top Left Wall',
            'Left Wall',
            'Bottom Left Wall',
            'Top Wall',
            'Centre Wall',
            'Bottom Wall',
            'Top Right Wall',
            'Right Wall',
            'Bottom Right Wall',
        ),
    },
}


def set_stats(stats, obj):
    for s in stats:
        v = stats[s]
        if s in SCALABLE_VALUES:
            v = round(v * obj.resourcemgr.scale)
        setattr(obj, s, v)


def set_unit_stats(unit):
    stats = UNIT_STATS.get(unit.kind, {})
    set_stats(stats, unit)

    unit.image = unit.resourcemgr.get_unit_image(unit.kind)
    unit.die_fx = unit.resourcemgr.get_unit_sound(unit.kind, 'die')
    unit.move_fx = unit.resourcemgr.get_unit_sound(unit.kind, 'move')
    unit.fire_fx = unit.resourcemgr.get_unit_sound(unit.kind, 'fire')
    unit.target_fx = unit.resourcemgr.get_unit_sound(unit.kind, 'target')


def set_tile_stats(tile):
    stats = TILE_STATS.get(tile.sheet, {})
    set_stats(stats, tile)


def set_button_stats(button):
    stats = BUTTON_STATS.get(button.kind, {})
    set_stats(stats, button)
    button.image = button.resourcemgr.get_button_image(button.kind)
