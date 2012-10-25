from math import sqrt
from iancraft.constants import BLACK
from iancraft.constants import BLUE
from iancraft.constants import FLAGS
from iancraft.constants import GREEN
from iancraft.constants import MOUSE
from iancraft.constants import RED
from iancraft.constants import SELECT
from iancraft.constants import STATES
from iancraft.kinds import set_unit_stats
from iancraft.sprites import GameGroup
from iancraft.sprites import GameSprite
from iancraft.utils import calculate_volume
from iancraft.utils import distance
from pygame import draw
from pygame import mouse
from pygame import time
from pygame.rect import Rect
from pygame.locals import MOUSEBUTTONUP


class UnitManager(object):
    def __init__(self, resourcemgr, state=STATES.INGAME, team=None,
        level=None):
        self.resourcemgr = resourcemgr
        self.state = state
        self.team = team
        self.teams = []
        self.units = {}
        self.dudes = {}
        self.structs = {}
        self.selected = GameGroup()
        self.active = None
        if level:
            self.load_units(level)

    def load_units(self, filename):
        try:
            level = open(filename, 'r')
            line = level.readline().strip()
            while line != '[units]':
                line = level.readline().strip()

            line = level.readline().strip()
            while line and line != '[tiles]':
                l = line.split(' ')
                x = int(l[0]) * self.resourcemgr.scale
                y = int(l[1]) * self.resourcemgr.scale
                k = int(l[2])
                t = int(l[3])
                unit = Unit(x, y, k, self.resourcemgr, t, self)
                self.add(unit)
                line = level.readline().strip()
            self.teams = [t for t in self.units]
            level.close()
        except IOError:
            pass

    def add(self, unit):
        self.units.setdefault(unit.team, GameGroup()).add(unit)
        if unit.has_flag(FLAGS.DUDE):
            self.dudes.setdefault(unit.team, GameGroup()).add(unit)
        else:
            self.structs.setdefault(unit.team, GameGroup()).add(unit)

    def input(self, event, *args, **kwargs):
        if event.type == MOUSEBUTTONUP and event.button == MOUSE.LEFT:
            self.active = None
            self.selected.empty()
        for t in self.teams:
            self.units[t].input(event, *args, **kwargs)
        self.active = self.selected.sprites()[0] if len(self.selected) > 0 \
            else None

    def logic(self, camera, *args, **kwargs):
        for t in self.teams:
            for u in self.units[t]:
                u.die(camera)

        for t in self.teams:
            self.units[t].logic(*args, **kwargs)

        self.num_enemies = sum([len(self.units[t]) for t in self.teams if
            t != self.team])
        self.num_units = len(self.units[self.team])

    def render(self, *args, **kwargs):
        for t in self.teams:
            self.units[t].render(*args, **kwargs)

    def play_sounds(self, *args, **kwargs):
        for t in self.teams:
            self.units[t].play_sounds(*args, **kwargs)


class Unit(GameSprite):
    def __init__(self, x, y, kind, resourcemgr, team, mgr):
        super(Unit, self).__init__(x, y, kind, resourcemgr)
        self.team = team
        self.mgr = mgr
        set_unit_stats(self)
        self.rect = Rect(int(x), int(y), self.w, self.h)
        self.set_areas()
        self.area = self.areas[SELECT.NORM]
        self.health = self.max_health
        self.attack_time = 0
        self.shoot_time = 0
        self.x_speed = 0.0
        self.y_speed = 0.0
        self.x_target = None
        self.y_target = None
        self.target = None
        self.selected = False
        self.moving = False
        self.lazy_attacking = False
        self.mouse_over = False
        self.active_sounds = []
        self.camera_sounds = []

    def set_areas(self):
        self.areas = {}
        self.areas[SELECT.NORM] = Rect(0, 0, self.w, self.h)
        self.areas[SELECT.MOVING] = Rect(self.w, 0, self.w, self.h)
        self.areas[SELECT.FIRING] = Rect(0, self.h, self.w, self.h)
        self.areas[SELECT.DUNNO] = Rect(self.w, self.h, self.w, self.h)

    def set_speed(self, x, y):
        self.x_target = x - (self.w / 2.0)
        self.y_target = y - (self.h / 2.0)
        self.moving = True

        if self.x_target > self.x:
            self.x_speed = self.speed
        if self.x_target < self.x:
            self.x_speed = -self.speed
        if self.y_target > self.y:
            self.y_speed = self.speed
        if self.y_target < self.y:
            self.y_speed = -self.speed

    def reset_speed(self):
        self.moving = False
        self.x_target = None
        self.y_target = None
        self.x_speed = 0.0
        self.y_speed = 0.0

    def hurt(self, atk):
        self.health -= atk

    def is_dead(self):
        return self.health <= 0

    def play_sounds(self, camera):
        if self is self.mgr.active:
            for s in self.active_sounds:
                s.play()
        v = calculate_volume(self.rect, camera)
        if v > 0:
            for s in self.camera_sounds:
                s.set_volume(v)
                s.play()
        self.active_sounds = []
        self.camera_sounds = []

    def find_area(self):
        if self.moving:
            self.area = self.areas[SELECT.MOVING]
        elif self.shoot_time:
            if time.get_ticks() - self.shoot_time >= self.shoot_delay:
                self.shoot_time = 0
            else:
                self.area = self.areas[SELECT.FIRING]
        else:
            self.area = self.areas[SELECT.NORM]

    def draw_select_box(self, camera):
        if self.selected:
            self.resourcemgr.screen.lock()
            dx = self.w / 10
            dy = self.h / 10
            draw.lines(self.resourcemgr.screen, BLUE, False, (
                (self.rect.x - camera.rect.x + 3,
                    self.rect.y - camera.rect.y + 3 + dy),
                (self.rect.x - camera.rect.x + 3,
                    self.rect.y - camera.rect.y + 3),
                (self.rect.x - camera.rect.x + 3 + dx,
                    self.rect.y - camera.rect.y + 3),
            ), 2)
            draw.lines(self.resourcemgr.screen, BLUE, False, (
                (self.rect.x - camera.rect.x - 3 + self.w - dx,
                    self.rect.y - camera.rect.y + 3),
                (self.rect.x - camera.rect.x - 3 + self.w,
                    self.rect.y - camera.rect.y + 3),
                (self.rect.x - camera.rect.x - 3 + self.w,
                    self.rect.y - camera.rect.y + 3 + dy),
            ), 2)
            draw.lines(self.resourcemgr.screen, BLUE, False, (
                (self.rect.x - camera.rect.x - 3 + self.w,
                    self.rect.y - camera.rect.y - 3 + self.h - dy),
                (self.rect.x - camera.rect.x - 3 + self.w,
                    self.rect.y - camera.rect.y - 3 + self.h),
                (self.rect.x - camera.rect.x - 3 + self.w - dx,
                    self.rect.y - camera.rect.y - 3 + self.h),
            ), 2)
            draw.lines(self.resourcemgr.screen, BLUE, False, (
                (self.rect.x - camera.rect.x + 3 + dx,
                    self.rect.y - camera.rect.y - 3 + self.h),
                (self.rect.x - camera.rect.x + 3,
                    self.rect.y - camera.rect.y - 3 + self.h),
                (self.rect.x - camera.rect.x + 3,
                    self.rect.y - camera.rect.y - 3 + self.h - dy),
            ), 2)
            self.resourcemgr.screen.unlock()

    def draw_health_bar(self, camera):
        if self.selected or self.mouse_over:
            black_rect = Rect(self.rect.x - camera.rect.x,
                self.rect.y - camera.rect.y, self.w, 6)
            red_rect = Rect(self.rect.x - camera.rect.x + 1,
                self.rect.y - camera.rect.y + 1, self.w - 2, 4)
            green_rect = Rect(self.rect.x - camera.rect.x + 1,
                self.rect.y - camera.rect.y + 1,
                (self.w - 2) * (self.health / float(self.max_health)), 4)
            self.resourcemgr.screen.lock()
            draw.rect(self.resourcemgr.screen, BLACK, black_rect, 0)
            draw.rect(self.resourcemgr.screen, RED, red_rect, 0)
            draw.rect(self.resourcemgr.screen, GREEN, green_rect, 0)
            self.resourcemgr.screen.unlock()

    def die(self, camera):
        if self.is_dead():
            self.kill()
            v = calculate_volume(self.rect, camera)
            if v > 0:
                self.die_fx.set_volume(v)
                self.die_fx.play()

    def input(self, event, camera, mouse_rect, tilemgr):
        x, y = mouse.get_pos()
        x += camera.rect.x
        y += camera.rect.y
        self.mouse_over = self.rect.collidepoint(x, y)

        if event.type == MOUSEBUTTONUP:
            if event.button == MOUSE.LEFT:
                include = True
                if self.rect.colliderect(mouse_rect):
                    if self.team != self.mgr.team and \
                        len(self.mgr.selected) > 0:
                        include = False
                    elif self.team == self.mgr.team:
                        rem = []
                        for u in self.mgr.selected:
                            if u.team != self.mgr.team:
                                u.selected = False
                                rem.append(u)
                        self.mgr.selected.remove(*rem)

                        if self.has_flag(FLAGS.STRUCT):
                            for u in self.mgr.selected:
                                if u.has_flag(FLAGS.DUDE):
                                    include = False
                                    break
                        elif self.has_flag(FLAGS.DUDE):
                            rem = []
                            for u in self.mgr.selected:
                                if u.has_flag(FLAGS.STRUCT):
                                    u.selected = False
                                    rem.append(u)
                            self.mgr.selected.remove(*rem)
                else:
                    include = False

                if include:
                    self.selected = True
                    self.mgr.selected.add(self)
                else:
                    self.selected = False
                    self.mgr.selected.remove(self)
            elif self.team == self.mgr.team and event.button == MOUSE.RIGHT \
                and self.selected:
                self.lazy_attacking = False
                found = False
                if self.has_flag(FLAGS.CAN_FIRE):
                    for t in self.mgr.teams:
                        if t == self.team:
                            continue
                        for u in self.mgr.units[t]:
                            if u.rect.collidepoint(x, y):
                                self.target = u
                                found = True
                                break
                        if found:
                            self.active_sounds.append(self.target_fx)
                            break

                if self.has_flag(FLAGS.CAN_MOVE) and not found:
                    self.set_speed(x, y)
                    self.target = None
                    self.active_sounds.append(self.move_fx)

                if self.has_flag(FLAGS.CAN_BUILD) and not found:
                    unit = Unit(x - 25, y - 25, self.buildables[0],
                        self.resourcemgr, self.team, self.mgr)
                    if not unit.get_collisions(tilemgr.walls,
                        *self.mgr.units.values()):
                        self.mgr.add(unit)

    def logic(self, ticks, tilemgr):
        if self.has_flag(FLAGS.CAN_FIRE):
            if self.target is not None:
                if self.target.is_dead() or (self.lazy_attacking and distance(
                    self.x, self.y, self.target.x,
                    self.target.y) > self.range * 2.5):
                    self.lazy_attacking = False
                    self.target = None
                    self.reset_speed()
                elif distance(self.x, self.y, self.target.x,
                    self.target.y) <= self.range:
                    if self.moving:
                        self.reset_speed()
                    if time.get_ticks() - self.attack_time >= \
                        self.attack_delay:
                        self.shoot_time = time.get_ticks()
                        self.attack_time = time.get_ticks()
                        self.camera_sounds.append(self.fire_fx)
                        self.target.hurt(self.atk)
                else:
                    self.set_speed(self.target.x, self.target.y)
            elif not self.moving:
                found = False
                for t in self.mgr.teams:
                    if t == self.team:
                        continue
                    for u in self.mgr.units[t]:
                        if distance(self.x, self.y, u.x, u.y) <= \
                            self.range * 2:
                            self.target = u
                            self.lazy_attacking = True
                            found = True
                            break
                    if found:
                        break

        if self.has_flag(FLAGS.CAN_MOVE) and self.moving:
            x_part = self.x_speed * (ticks / 1000.0)
            y_part = self.y_speed * (ticks / 1000.0)
            x_old = self.x
            y_old = self.y
            rx_old = self.rect.x
            ry_old = self.rect.y
            x_delta = 0.0
            y_delta = 0.0

            if self.x_target:
                if abs(self.x_target - self.x) <= abs(x_part):
                    x_delta = self.x_target - self.x
                elif abs(self.y_target - self.y) > abs(y_part):
                    x_delta = x_part / sqrt(2.0)
                else:
                    x_delta = x_part
            self.x += x_delta
            self.rect.x = int(self.x)
            if self.get_collisions(tilemgr.walls, *self.mgr.units.values()):
                self.x = x_old
                self.rect.x = rx_old

            if self.y_target:
                if abs(self.y_target - self.y) <= abs(y_part):
                    y_delta = self.y_target - self.y
                elif abs(self.x_target - self.x) > abs(x_part):
                    y_delta = y_part / sqrt(2.0)
                else:
                    y_delta = y_part
            self.y += y_delta
            self.rect.y = int(self.y)
            if self.get_collisions(tilemgr.walls, *self.mgr.units.values()):
                self.y = y_old
                self.rect.y = ry_old

            if self.x_target == self.x and self.y_target == self.y:
                self.reset_speed()

    def render(self, camera=None):
        self.find_area()
        if not camera:
            self.resourcemgr.screen.blit(self.image, self.rect, self.area)
            self.draw_select_box(camera)
            self.draw_health_bar(camera)
        elif self.rect.colliderect(camera):
            pos = Rect(self.rect.x - camera.rect.x,
                self.rect.y - camera.rect.y, self.rect.w, self.rect.h)
            self.resourcemgr.screen.blit(self.image, pos, self.area)
            self.draw_select_box(camera)
            self.draw_health_bar(camera)
