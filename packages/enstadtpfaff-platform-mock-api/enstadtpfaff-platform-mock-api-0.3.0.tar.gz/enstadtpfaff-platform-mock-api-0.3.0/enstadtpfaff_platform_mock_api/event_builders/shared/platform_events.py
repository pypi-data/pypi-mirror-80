from enstadtpfaff_platform_mock_api import Event
from enstadtpfaff_platform_mock_api.util import TopicUtil


class PlatformEvents:
    SHARED_TOPIC_ID = "platform-events"
    HELLO_PLATFORM_TOPIC = TopicUtil.shared_topic(SHARED_TOPIC_ID, "hello-platform")
    GOODBYE_PLATFORM_TOPIC = TopicUtil.shared_topic(SHARED_TOPIC_ID, "goodbye-platform")
    ALIVE_PING_TOPIC = TopicUtil.shared_topic(SHARED_TOPIC_ID, "alive-ping")

    @staticmethod
    def hello_platform(name: str, description: str) -> Event:
        return Event(
            topic=PlatformEvents.HELLO_PLATFORM_TOPIC,
            payload={
                'name': name,
                'description': description
            }
        )

    @staticmethod
    def goodbye_platform(name: str) -> Event:
        return Event(
            topic=PlatformEvents.GOODBYE_PLATFORM_TOPIC,
            payload={
                'name': name
            }
        )

    @staticmethod
    def alive_ping(name: str) -> Event:
        return Event(
            topic=PlatformEvents.ALIVE_PING_TOPIC,
            payload={
                'name': name
            }
        )
