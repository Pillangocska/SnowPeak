"""Initializing command descriptor related tests."""

import unittest
from datetime import datetime

from ski_lift.core.command.descriptor import CommandDescriptor
from tests.entity.command.descriptor.command_descriptor.concrete_descriptor import \
    ConcreteCommandDescriptor


class CommandDescriptorInitTestCase(unittest.TestCase):
    """Engine state related unit tests."""

    test_data: dict = {
        'user_card': 'abc123',
        'time': datetime.now(),
        'delay': 15,
    }

    def test_id_increment(self):
        for x in range(1, 10):
            command: CommandDescriptor = ConcreteCommandDescriptor(**self.test_data)
            self.assertEqual(command.id, x)
