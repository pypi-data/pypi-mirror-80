from paho.mqtt.client import Client, MQTTMessage

from .event import Event


class EventBroker:
    def __init__(self,
                 mqtt_address: str,
                 mqtt_username: str,
                 mqtt_password: str,
                 client_id: str,
                 event_handler=None):
        self._client = Client(client_id=client_id, clean_session=True)
        self._client.username_pw_set(username=mqtt_username, password=mqtt_password)
        self._client.tls_set()
        self._client.connect(host=mqtt_address, port=8883)
        self._event_handler = event_handler
        self._client.message_callback_add('#', self._on_message)

        # TODO reconnect + what about the subscriptions?
        self._client.loop_start()

    def _on_message(self, client: Client, userdata, message: MQTTMessage):
        event = Event(message.topic, message.payload.decode("utf8"))
        if self._event_handler is not None:
            self._event_handler(event)

    def subscribe(self, topic: str) -> None:
        self._client.subscribe(topic=topic)  # TODO check reconnect resubscribe...

    def unsubscribe(self, topic: str) -> None:
        self._client.unsubscribe(topic)

    def disconnect(self) -> None:
        self._client.disconnect()

    def publish(self, event: Event) -> None:
        self._client.publish(event.topic, event.payload)
