"""Engine related unit tests."""

import unittest

from ski_lift.core.engine import Engine, EngineState


class EngineStateTestCase(unittest.TestCase):
    """Engine state related unit tests."""

    def setUp(self):
        self.engine = Engine()

    def test__state_is_stopped__after_init(self):
        self.assertEqual(self.engine.state, EngineState.STOPPED)

    def test__state_is_max_steam__after_max_steam(self):
        self.engine.max_steam()
        self.assertEqual(self.engine.state, EngineState.MAX_STEAM)

    def test__state_is_full_steam__after_full_steam(self):
        self.engine.full_steam()
        self.assertEqual(self.engine.state, EngineState.FULL_STEAM)

    def test__state_is_half_steam__after_half_steam(self):
        self.engine.half_steam()
        self.assertEqual(self.engine.state, EngineState.HALF_STEAM)

    def test__state_is_stopped__after_stop(self):
        # emulate different state
        self.engine._state = EngineState.FULL_STEAM

        self.engine.stop()
        self.assertEqual(self.engine.state, EngineState.STOPPED)