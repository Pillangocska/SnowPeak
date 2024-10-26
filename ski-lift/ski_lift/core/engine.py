"""Entity representation of a ski lift engine."""

from enum import Enum, auto


class EngineState(Enum):
    """Engine state representation."""

    MAX_STEAM = auto()
    FULL_STEAM = auto()
    HALF_STEAM = auto()
    STOPPED = auto()

class Engine(object):
    """Entity representation of a ski lift engine."""

    def __init__(self):
        self._set_state(EngineState.STOPPED)

    @property
    def state(self) -> EngineState:
        return self._state
    
    def max_steam(self):
        self._set_state(EngineState.MAX_STEAM)

    def full_steam(self):
        self._set_state(EngineState.FULL_STEAM)
    
    def half_steam(self):
        self._set_state(EngineState.HALF_STEAM)

    def stop(self):
        self._set_state(EngineState.STOPPED)

    def _set_state(self, new_state: EngineState):
        self._state = new_state