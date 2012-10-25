from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame.sprite import spritecollide


class GameSprite(Sprite):
    def __init__(self, x, y, kind=None, resourcemgr=None):
        super(GameSprite, self).__init__()
        self.x = float(x)
        self.y = float(y)
        if kind is not None:
            self.kind = kind
        if resourcemgr is not None:
            self.resourcemgr = resourcemgr

    def has_flag(self, flag):
        return hasattr(self, 'flags') and self.flags & flag

    def get_collisions(self, *groups):
        sprites = []
        for g in groups:
            sprites.extend(spritecollide(self, g, False))
        return [s for s in sprites if s is not self]

    def input(self, *args, **kwargs):
        pass

    def logic(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        pass


class GameGroup(Group):
    def __init__(self):
        super(GameGroup, self).__init__()

    def play_sounds(self, *args, **kwargs):
        for s in self:
            s.play_sounds(*args, **kwargs)

    def input(self, *args, **kwargs):
        for s in self:
            s.input(*args, **kwargs)

    def logic(self, *args, **kwargs):
        for s in self:
            s.logic(*args, **kwargs)

    def render(self, *args, **kwargs):
        for s in self:
            s.render(*args, **kwargs)
