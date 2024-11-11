from typing import Any
import pika
from pika.exchange_type import ExchangeType
from time import sleep
from pika.connection import ConnectionParameters
from pika.channel import Channel
from pika.adapters import SelectConnection
from threading import Thread, Event
from typing import Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)


class PikaProducer(object):
    """."""

    def __init__(
        self,
        exchange: str,
        exchange_type: ExchangeType,
        connection_parameters: ConnectionParameters,
    ):
        self._exchange: str = exchange
        self._exchange_type: ExchangeType = exchange_type
        self._connection_parameters: ConnectionParameters = connection_parameters
        self._thread: Thread = None
        self._stop_event: Event = None
        self._connection: SelectConnection  = None
        self._channel: Channel = None
        self._pending_messages: List[Tuple] = []

    def connect(self) -> SelectConnection:
        return pika.SelectConnection(
            self._connection_parameters,
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )

    def on_connection_open(self, connection) -> None:
        self._connection = connection
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_connection_open_error(self, _unused_connection, err) -> None:
        self._connection.ioloop.call_later(5, self._connection.ioloop.stop)

    def on_connection_closed(self, _unused_connection, reason) -> None:
        self._channel = None
        if self._stopping:
            self._connection.ioloop.stop()
        else:
            self._connection.ioloop.call_later(5, self._connection.ioloop.stop)

    def on_channel_open(self, channel) -> None:
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_closed)
        self._channel.confirm_delivery(self.on_delivery_confirmation)
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type=self._exchange_type,
            callback=self.setup_exchange_ok,
        )

    def on_channel_closed(self, channel, reason) -> None:
        self._channel = None
        if not self._stopping:
            self._connection.close()

    def on_delivery_confirmation(self, method_frame) -> None:
        pass

    def setup_exchange_ok(self, _unused_frame) -> None:
        self._connection.ioloop.call_later(10, self.send_pending_messages)

    def send_pending_messages(self) -> None:
        for pending in self._pending_messages:
            self.publish_message(*pending)
        self._pending_messages.clear()
    
    def publish_message(self, routing_key: str, message: Any, headers: Optional[dict] = None) -> bool:
        if self._channel is None or not self._channel.is_open:
            self._pending_messages.append((routing_key, message, headers))
            return False
        self._channel.basic_publish(
            self._exchange,
            routing_key,
            message,
            properties=pika.BasicProperties(headers=headers or {}),
        )
        return True

    def run(self) -> None:
        while not self._stop_event.is_set():
            self._connection = None
            try:
                self._connection = self.connect()
                self._connection.ioloop.start()   
            except Exception as err:
                if self._connection is not None and not self._connection.is_closed:
                    self._connection.close()  # Close the connection if it exists and is not closed
                sleep(5)

    def start(self) -> None:
        if self._thread is None:
            self._thread = Thread(target=self.run)
            self._stop_event = Event()
            self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        self.close_channel()
        self.close_connection()
        self._thread.join()
        self._thread = None

    def close_channel(self) -> None:
        if self._channel is not None:
            self._channel.close()

    def close_connection(self) -> None: 
        if self._connection is not None:
            self._connection.close()
