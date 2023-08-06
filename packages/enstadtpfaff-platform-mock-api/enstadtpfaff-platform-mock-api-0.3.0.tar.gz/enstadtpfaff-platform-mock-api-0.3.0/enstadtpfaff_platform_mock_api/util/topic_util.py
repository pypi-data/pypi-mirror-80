from .constants import CONST
from .topic_type import TopicType


class TopicUtil:

    @staticmethod
    def shared_topic(shared_topic_id: str, *additional_segments: str):
        return TopicUtil._typed_topic(TopicType.SHARED, shared_topic_id, *additional_segments)

    @staticmethod
    def service_specific_topic(service_id: str, *additional_segments: str):
        return TopicUtil._typed_topic(TopicType.SERVICE_SPECIFIC, service_id, *additional_segments)

    @staticmethod
    def _typed_topic(topic_type: TopicType, topic_id: str, *additional_segments: str):
        return TopicUtil._combineTopicPaths(*[CONST.TOPIC_ROOT, topic_type.value, topic_id, *additional_segments])

    @staticmethod
    def _combineTopicPaths(*path_segments: str) -> str:
        return CONST.TOPIC_LEVEL_SEPARATOR.join(path_segments)
