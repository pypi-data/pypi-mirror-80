from .event import Event
from .event_broker import EventBroker
from .event_builders.shared import PlatformEvents


class PlatformMockApi:
    def __init__(self,
                 event_broker: EventBroker,
                 sender_name: str
                 ):
        self._event_broker = event_broker
        self._sender_name = sender_name

    @property
    def event_broker(self) -> EventBroker:
        return self._event_broker

    @property
    def sender_name(self):
        return self._sender_name

    def create_hello_platform_event(self, description: str) -> Event:
        return PlatformEvents.hello_platform(self.sender_name, description)

    def create_goodbye_platform_event(self) -> Event:
        return PlatformEvents.goodbye_platform(self.sender_name)

    def create_alive_ping_event(self) -> Event:
        return PlatformEvents.alive_ping(self.sender_name)
