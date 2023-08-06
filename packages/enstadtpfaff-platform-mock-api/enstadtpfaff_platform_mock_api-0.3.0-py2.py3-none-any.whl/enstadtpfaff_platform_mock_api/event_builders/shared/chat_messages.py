from enstadtpfaff_platform_mock_api import Event
from enstadtpfaff_platform_mock_api.util import TopicUtil


class ChatMessages:
    SHARED_TOPIC_ID = "chat-messages"
    CHAT_MESSAGES_TOPIC = TopicUtil.shared_topic(SHARED_TOPIC_ID)

    @staticmethod
    def chat_message(application_name: str, from_: str, to: str, message: str) -> Event:
        return Event(
            topic=ChatMessages.CHAT_MESSAGES_TOPIC,
            payload={
                'senderApplication': application_name,
                'from': from_,
                'to': to,
                'message': message
            }
        )
