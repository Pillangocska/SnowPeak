from ski_lift.app.entity.ski_lift_authorizer import SkiLiftAuthorizer
from ski_lift.app.entity.ski_lift_controller import SkiLiftController
from ski_lift.core.auth.authenticator.in_memory_authenticator import InMemoryAuthenticator
from ski_lift.core.engine import Engine
from ski_lift.core.monitor.logger.file import FileCommandLogger
from ski_lift.core.monitor.logger.rabbit_mq import RabbitMQCommandLogger
from ski_lift.core.view.cli_view import CommandLineInterfaceView
import sys
from ski_lift.core.command.descriptor.serializer.pretty_string import PrettyStringDescriptorSerializer
from ski_lift.core.command.descriptor.serializer.json_bytes import JSONBytesDescriptorSerializer
from ski_lift.core.command.result.serializer.pretty_string import PrettyResultStringSerializer
from ski_lift.core.command.result.serializer.json_bytes import JSONBytesResultSerializer
from ski_lift.core.remote.rabbitmq.pika_client import PikaClient
import pika
from ski_lift.core.remote.suggestion.rabbit_mq_suggestion_forwarder import RabbitMQSuggestionForwarder


def main() -> int:
    # create an example authenticator and register a card number
    authenticator = InMemoryAuthenticator()
    authenticator.add('secret')

    # create a controller which needs an engine and an authorizer
    controller = SkiLiftController(engine=Engine(), authorizer=SkiLiftAuthorizer(authenticator=authenticator))

    

    command_logger = FileCommandLogger(PrettyStringDescriptorSerializer(), PrettyResultStringSerializer())
    command_logger.attach_to(controller)

    # rabbit mq logger
    pika_client = PikaClient(connection_parameters=pika.ConnectionParameters(host='localhost'))

    rabbit_logger = RabbitMQCommandLogger(JSONBytesDescriptorSerializer(), JSONBytesResultSerializer(), pika_client)
    rabbit_logger.attach_to(controller)

    # create a cli view with the controller and start accepting user input
    cli = CommandLineInterfaceView(controller=controller)
    suggestion =  RabbitMQSuggestionForwarder(view=cli, lift_id=sys.argv[1])
    suggestion.start()




    controller.start()
    cli.start_handling_user_inputs()
    controller.stop()
    suggestion.stop()
    return 0


if __name__ == '__main__':
    sys.exit(main())