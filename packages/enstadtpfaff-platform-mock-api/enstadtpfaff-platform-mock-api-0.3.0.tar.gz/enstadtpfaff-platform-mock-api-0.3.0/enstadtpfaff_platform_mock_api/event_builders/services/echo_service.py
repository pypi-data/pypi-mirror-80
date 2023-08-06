from enstadtpfaff_platform_mock_api import Event
from enstadtpfaff_platform_mock_api.util import TopicUtil


class EchoService:
    SERVICE_ID = 'pm-echo-service'
    PING_TOPIC = TopicUtil.service_specific_topic(SERVICE_ID, 'ping')

    @staticmethod
    def ping(payload: str):
        return Event(EchoService.PING_TOPIC, payload)
