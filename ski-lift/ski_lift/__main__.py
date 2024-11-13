"""Entry point for the ski lift component."""

import sys

from ski_lift.core.utils import get_lift_id_or_exit
from ski_lift.core.view.cli_view import CommandLineInterfaceView
from ski_lift.use_cases import create_controller, create_pika_producer, setup_sensor, attach_loggers_to


def main() -> int:
    lift_id: str = get_lift_id_or_exit()

    with create_pika_producer() as producer:
        with create_controller(lift_id=lift_id, producer=producer) as controller:
            attach_loggers_to(controller, producer)            
            # todo: refactor to be inside controller
            setup_sensor(lift_id=lift_id, pika_producer=producer)
            cli = CommandLineInterfaceView(controller=controller)
            cli.start_handling_user_inputs()
            return 0


if __name__ == '__main__':
    sys.exit(main())