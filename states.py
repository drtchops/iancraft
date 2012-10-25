from pygame.locals import QUIT
from constants import STATES
from utils import set_next_state


class State(object):
    def __init__(self, resourcemgr):
        self.resourcemgr = resourcemgr

    def input(self, event, next_state):
        if event.type == QUIT:
            next_state = set_next_state(next_state, STATES.EXIT)
        return next_state

    def logic(self, clock, next_state):
        return next_state

    def render(self):
        pass
