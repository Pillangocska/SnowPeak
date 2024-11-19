"""Entity representation of a ski lift engine."""

from enum import Enum, auto

from traitlets import ValidateHandler


class EngineState(Enum):
    """Engine state representation."""

    MAX_STEAM = 'MAX_STEAM'
    FULL_STEAM = 'FULL_STEAM'
    HALF_STEAM = 'HALF_STEAM'
    STOPPED = 'STOPPED'

class Engine(object):
    """Entity representation of a ski lift engine."""

    def __init__(self, state: EngineState = EngineState.STOPPED):
        self._set_state(state)

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
        if isinstance(new_state, str):
            new_state = self._parse_state(new_state)
        self._state = new_state

    def _parse_state(self, state: str) -> EngineState:
        try:
            return EngineState(state)
        except ValueError:
            return EngineState.STOPPED